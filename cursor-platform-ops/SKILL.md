---
name: cursor-platform-ops
description: "Use when operating Cursor IDE as an agent platform — choosing the right config surface (rules, skills, hooks, settings, MCP, automations), switching workspaces, or using cursor-app-control MCP tools."
disable-model-invocation: true
version: 1.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cursor, agent, configuration, mcp, workspace]
    related_skills: [make-skill, init, mcp-server-patterns]
---

# Cursor Platform Ops

## Overview

Cursor is more than an editor — it is an agent platform with several independent configuration surfaces. Each surface solves a different problem: persistent guidance (rules), reusable workflows (skills), event-driven guardrails (hooks), editor behavior (settings), external integrations (MCP), and scheduled/cloud agents (Automations).

This skill is the routing layer. It tells the agent **which surface to use**, **where files live**, and **how to drive Cursor from chat** via the `cursor-app-control` MCP server. For deep authoring on a single surface, defer to the specialized built-in skills listed below.

## When to Use

**Use this skill when:**
- The user asks how Cursor configuration works or where something belongs
- You need to pick between rules, skills, hooks, settings, user rules, or MCP
- The task involves switching workspace roots, bootstrapping a new project, or opening Glass UI surfaces
- You are unsure which Cursor-specific skill or file path applies

**Don't use for:**
- Writing a single `.mdc` rule file → use built-in `create-rule` skill
- Authoring or updating a skill → use `make-skill` (custom skills) or built-in `create-skill` (Cursor skills)
- Editing `settings.json` → use built-in `update-cursor-settings`
- Creating hooks → use built-in `create-hook`
- Creating Cursor Automations → use built-in `automate` skill
- General coding in the user's repo (unrelated to Cursor itself)

---

## Configuration Surface Router

When the user wants persistent agent behavior, pick **one primary surface** first. Combine surfaces only when they solve different layers (e.g., a rule for style + a hook for shell gating).

| User intent | Surface | Scope | Location | Specialized skill |
|-------------|---------|-------|----------|-------------------|
| Coding standards, file-specific conventions | **Project rules** | Repo | `.cursor/rules/*.mdc` | `create-rule` |
| Global preferences across all projects | **User rules** | User | Cursor Settings → Rules (managed via MCP) | this skill § User Rules |
| Reusable multi-step workflows | **Skills** | User or repo | `~/.skills/`, `~/.cursor/skills/`, `.cursor/skills/` | `make-skill`, `create-skill` |
| Block/audit/format around agent events | **Hooks** | User or repo | `~/.cursor/hooks.json`, `.cursor/hooks.json` | `create-hook` |
| Font, theme, format-on-save, keybindings | **Settings** | User or workspace | `settings.json`, `.vscode/settings.json` | `update-cursor-settings` |
| Connect external APIs, databases, SaaS | **MCP servers** | User/team/project | `~/.cursor/mcp.json`, dashboard | `mcp-server-patterns` |
| Scheduled or event-driven cloud agents | **Automations** | Cloud | cursor.com dashboard + Glass UI | `automate` |
| Agent attribution / CLI behavior | **CLI config** | User | `~/.cursor/cli-config.json` | `update-cursor-settings` |

### Decision flow

```
Need behavior on every chat in this repo?
  ├─ Yes, about code patterns → project rule (.mdc)
  ├─ Yes, about agent events (shell/MCP/edits) → hook
  └─ Yes, a full workflow the agent should follow → project skill (.cursor/skills/)

Need behavior in every project for this user?
  ├─ Short preference text → user rule (cursor_dialog)
  ├─ Editor UI behavior → settings.json
  └─ Reusable workflow → ~/.skills/ or ~/.cursor/skills/

Need external data or actions?
  └─ MCP server (authenticate before Automations prefill)

Need recurring cloud execution?
  └─ Cursor Automation (Agents Window + automate skill)
```

---

## Directory Map

### User-level (`~/.cursor/`)

| Path | Purpose |
|------|---------|
| `~/.cursor/skills/` | Personal Cursor Agent Skills (discovered by Cursor) |
| `~/.cursor/skills-cursor/` | **Built-in Cursor skills — do not write here** |
| `~/.cursor/hooks.json` + `~/.cursor/hooks/` | User-wide hooks |
| `~/.cursor/mcp.json` | Local MCP server definitions |
| `~/.cursor/mcps/<folder>/` | Runtime MCP metadata (`SERVER_METADATA.json`, tool descriptors) |
| `~/.cursor/cli-config.json` | Cursor CLI agent configuration |
| `~/.cursor/projects/<id>/` | Per-session agent state (terminals, MCP cache) |

### Custom skills library (`~/.skills/`)

| Path | Purpose |
|------|---------|
| `~/.skills/<name>/SKILL.md` | Authoritative custom skill store (git-backed) |
| `~/.skills/make-skill/` | Meta-skill for creating or updating custom skills |

Agent runtimes may symlink `~/.skills/` into `~/.cursor/skills/` or `~/.claude/skills/`. When creating a **custom** skill the user owns, write to `~/.skills/` per `make-skill`.

### Project-level (`.cursor/`)

| Path | Purpose |
|------|---------|
| `.cursor/rules/*.mdc` | Project rules with optional `globs` / `alwaysApply` |
| `.cursor/skills/<name>/SKILL.md` | Project-scoped skills (shared via git) |
| `.cursor/hooks.json` + `.cursor/hooks/` | Project hooks |
| `.cursor/mcp.json` | Project MCP overrides |
| `AGENTS.md` | Optional agent context at repo root (referenced by rules tooling) |

### Editor settings

| OS | User settings path |
|----|-------------------|
| macOS | `~/Library/Application Support/Cursor/User/settings.json` |
| Linux | `~/.config/Cursor/User/settings.json` |
| Windows | `%APPDATA%\Cursor\User\settings.json` |

Workspace settings: `.vscode/settings.json` in the project root.

---

## cursor-app-control MCP

Available in the **Agents Window** (Glass). Read tool schemas from `~/.cursor/projects/<session>/mcps/cursor-app-control/tools/` before calling.

| Tool | When to use |
|------|-------------|
| `move_agent_to_root` | Switch agent to a different directory; runs `git fetch` + ff-merge on destination branch |
| `move_agent_to_cloned_root` | Switch to a sibling `cursorfs-clone` under `~/.cursor/cursorfs-clone/` — skips fetch |
| `create_project` | Create directory + `git init`; pair with `move_agent_to_root` |
| `open_automation` | Open Glass Automations UI with optional `prefillWorkflowData` |
| `cursor_dialog` | Manage **user rules** (`item=rule`, `scope=user`, `action=list|add|update|remove`) |
| `rename_chat` | Set the current conversation tab title (≤200 chars) |

### Workspace switch workflow

1. Confirm destination path exists (or call `create_project` first).
2. If destination is a **fresh cursorfs clone** on the same branch → `move_agent_to_cloned_root`.
3. Otherwise → `move_agent_to_root` with absolute `rootPath` (or `rootPaths` for multi-root).
4. After move, re-read project context; terminal cwd and git state follow the new root.

### Bootstrap new project workflow

```
create_project({ path: "/absolute/path/to/new-app" })
  → move_agent_to_root({ rootPath: "/absolute/path/to/new-app" })
  → /init   (optional: generate README.md + AGENTS.md + CLAUDE.md)
```

---

## User Rules vs Project Rules

Both steer the agent, but they differ in scope and authoring path.

| | User rules | Project rules |
|---|-----------|---------------|
| **Scope** | All projects for this user | Current repository |
| **Storage** | Cursor cloud / Settings UI | `.cursor/rules/*.mdc` in git |
| **Author via agent** | `cursor_dialog` MCP (`action=list` first to avoid duplicates) | Write `.mdc` files directly |
| **Best for** | Personal preferences ("always use bun", commit style) | Team conventions, file-type patterns |

**User rule MCP pattern:**

1. `cursor_dialog({ item: "rule", scope: "user", action: "list" })`
2. If no duplicate → `action: "add", content: "...", title: "..."`
3. To edit → `action: "update", id: "<id>", content: "..."`

Do **not** put team coding standards in user rules when the repo should own them — use project rules so teammates share the same guidance.

---

## Skills: Three Stores

| Store | Path | Write? | Use case |
|-------|------|--------|----------|
| Custom library | `~/.skills/` | Yes | Durable, git-versioned workflows (`make-skill` format) |
| Personal Cursor | `~/.cursor/skills/` | Yes | Cursor-native discovery |
| Project | `.cursor/skills/` | Yes | Team-shared workflows in repo |
| Built-in | `~/.cursor/skills-cursor/` | **Never** | Cursor-managed (`create-rule`, `automate`, etc.) |

When the user invokes `/make-skill`, create under `~/.skills/`. When they say "make this a Cursor skill for my team", use `.cursor/skills/`.

---

## MCP Essentials

MCP servers extend the agent with tools (GitHub, Linear, Supabase, browser, etc.).

### Inspect catalog

```bash
ls ~/.cursor/mcps/
cat ~/.cursor/mcps/<folder>/SERVER_METADATA.json
```

Key fields in `SERVER_METADATA.json`:
- `serverIdentifier` — runtime folder name (e.g. `plugin-linear-linear`)
- `serverName` — display name for Automations prefill (e.g. `Linear`)

### Authentication

If `~/.cursor/mcps/<folder>/STATUS.md` says the server needs authentication, call `mcp_auth` for that server **before** relying on its tools or prefilling Automations. Unauthenticated MCP rows block Automation saves.

### Automations eligibility

Only **dashboard-backed** MCP servers (identifiers starting with `dashboard-team-`, `dashboard-`, or `plugin-`) appear in the Automations editor catalog. Local servers like `cursor-app-control` and `cursor-ide-browser` are **not** eligible for Automation `mcp` actions.

---

## Common Workflows

### 1. "Make the agent always do X in this repo"

1. If X is a short convention → project rule (`.cursor/rules/x.mdc`)
2. If X is a multi-step procedure → project skill (`.cursor/skills/x/SKILL.md`)
3. If X must run on shell/MCP/edit events → hook (`.cursor/hooks.json`)

### 2. "Remember this preference everywhere"

1. List existing user rules via `cursor_dialog`
2. Add or update the user rule
3. Do **not** also duplicate in `settings.json` unless it is an editor UI setting

### 3. "Work in a different folder / new repo"

1. `create_project` if needed
2. `move_agent_to_root` or `move_agent_to_cloned_root`
3. Verify with `git status` in the new root

### 4. "Set up a scheduled Cursor agent"

1. Confirm running in Agents Window (`open_automation` available)
2. Load built-in `automate` skill — do not improvise YAML by hand
3. Authenticate MCP integrations in chat before editor handoff

### 5. "Change editor theme / font / format on save"

1. Load `update-cursor-settings`
2. Read existing `settings.json`, patch only requested keys
3. Tell user if window reload is needed

---

## Common Pitfalls

1. **Writing to `~/.cursor/skills-cursor/`** — reserved for Cursor built-ins; user skills go in `~/.skills/` or `~/.cursor/skills/`.

2. **Using `move_agent_to_root` on cursorfs clones** — fails with "Remote branch not found on origin" for local-only branches; use `move_agent_to_cloned_root` instead.

3. **Project hooks with wrong script paths** — project hooks run from repo root (`.cursor/hooks/...`); user hooks run from `~/.cursor/` (`./hooks/...`).

4. **Confusing user rules and project rules** — team standards belong in `.cursor/rules/`; personal prefs belong in user rules.

5. **Prefilling Automations with local MCP servers** — `cursor-app-control` and browser MCPs won't resolve in the Automations editor; use dashboard-backed servers only.

6. **Skipping `cursor_dialog` list before add** — creates duplicate user rules with overlapping guidance.

7. **Putting workflows in memory/rules** — multi-step procedures belong in skills, not one-line user rules or always-on rules.

8. **Editing settings without reading first** — clobbering `settings.json` removes unrelated user config; always read-merge-write.

---

## Verification Checklist

- [ ] Correct surface chosen (rule vs skill vs hook vs settings vs MCP)
- [ ] Files written to the intended scope (user vs project vs `~/.skills/`)
- [ ] No writes under `~/.cursor/skills-cursor/`
- [ ] For workspace moves: absolute paths used; correct move tool (clone vs generic)
- [ ] For user rules: listed existing rules before add/update
- [ ] For MCP-dependent Automations: server authenticated and dashboard-eligible
- [ ] For settings changes: JSON valid; unrelated keys preserved
- [ ] Skill committed to `~/.skills` git when creating custom skills
