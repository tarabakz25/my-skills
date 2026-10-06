---
name: init
description: "Use when a new or existing project is missing README.md, AGENTS.md, and/or CLAUDE.md. Analyze the codebase and generate them from detected stack, commands, structure, and conventions."
disable-model-invocation: true
version: 1.1.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [init, readme, agents-md, claude-md, onboarding, project]
    related_skills: [codebase-onboarding, prompt-optimizer]
---

# Init

## Overview

New projects often ship code before docs. This skill inspects manifests, directory layout, scripts, tests, and recent git history, then writes **README.md** (for humans), **AGENTS.md** (canonical agent context), and **CLAUDE.md** (imports AGENTS.md for Claude Code) at the project root. Content is inferred from the repo — not copied from templates verbatim.

For a full onboarding narrative (architecture map, request lifecycle, "where to look" tables), also load `codebase-onboarding`. This skill stops at generating the docs files.

## When to Use

**Use this skill when:**
- User invokes `/init` or asks to "init project docs"
- A new project has no `README.md`, `AGENTS.md`, and/or `CLAUDE.md`
- User scaffolded a repo and wants agent/human context generated from code

**Don't use for:**
- Files already exist and user only wants edits (enhance in place; don't overwrite)
- Deep architecture tour without writing files (use `codebase-onboarding`)
- Open-source packaging with LICENSE/CONTRIBUTING (use `opensource-pipeline`)

## Command Interface

| Command | Action |
|---------|--------|
| `/init` | Generate missing README.md, AGENTS.md, and CLAUDE.md in current project root |
| `/init --readme` | Generate README.md only if missing |
| `/init --agents` | Generate AGENTS.md only if missing |
| `/init --claude` | Generate CLAUDE.md only if missing |
| `/init --force` | Regenerate even when files exist (confirm with user first) |

Default project root: current working directory. Accept explicit path if user provides one.

Legacy alias: `/project-init` → treat as `/init`.

---

## Workflow

### Step 1 — Check Existing Files

```bash
test -f README.md && echo "README exists" || echo "README missing"
test -f AGENTS.md && echo "AGENTS exists" || echo "AGENTS missing"
test -f CLAUDE.md && echo "CLAUDE exists" || echo "CLAUDE missing"
```

| State | Action |
|-------|--------|
| All missing | Generate README + AGENTS + CLAUDE |
| Some missing | Generate only the missing files |
| All exist, no `--force` | Stop; offer to enhance sections instead |
| Any exist + `--force` | Read existing file first, merge useful content, then rewrite |

If a file exists, **read it before writing**. Preserve user-written sections (license, deployment notes, team rules).

### Step 2 — Reconnaissance

Run the detector script from the project root:

```bash
python3 ~/.skills/init/scripts/detect_project.py .
```

Use the JSON plus targeted reads. In parallel, gather:

```
1. Manifests — package.json, go.mod, Cargo.toml, pyproject.toml, etc.
2. Config fingerprints — next.config.*, vite.config.*, tsconfig.json, Dockerfile
3. Entry points — main.*, index.*, cmd/, src/app/
4. Top-level directories — ignore node_modules, .git, dist, build, vendor
5. Test layout — tests/, __tests__/, *_test.go, *.test.ts
6. CI — .github/workflows/, Makefile targets
7. Git signals — recent commit subjects, branch style (skip if no history)
```

**Rules:**
- Prefer Glob/Grep over reading every file
- Trust code over config when they conflict
- If unknown, say "Could not detect …" — do not invent commands

For deeper mapping (data flow, architecture diagram), load `~/.skills/codebase-onboarding/SKILL.md` Phase 2–3 — but still output only the docs files.

### Step 3 — Derive Content

From recon, fill these fields before writing:

| Field | Source |
|-------|--------|
| Project name | package name, Cargo name, go module tail, or directory name |
| One-line description | package.json `description`, pyproject summary, or infer from README stub / main entry |
| Stack | manifests + dependencies + config files |
| Install command | `npm install`, `pnpm install`, `pip install -e .`, `cargo build`, etc. |
| Dev command | first `dev`/`start` script, Makefile `dev`, framework default |
| Test command | `npm test`, `pytest`, `go test ./...`, `cargo test` |
| Build command | `npm run build`, `make build`, `go build ./...` |
| Lint command | `npm run lint`, `ruff check`, `golangci-lint run` if configured |
| Structure map | top-level dirs → purpose (only non-obvious ones) |
| Conventions | naming from samples, error handling pattern, test file suffix |
| Do not do | project-specific guardrails (no secrets in repo, migration rules, etc.) |

Command priority for Node projects:

```text
dev  → scripts.dev || scripts.start
test → scripts.test
lint → scripts.lint
build → scripts.build
```

If a command is not detectable, omit that section instead of guessing.

### Step 4 — Write README.md

Target: **human readers** — what it is, how to install, run, test, build, and where things live.

Use structure from `~/.skills/init/templates/README.md.tpl` as an outline, not a fill-in-the-blank. Write complete prose and real commands.

**README must include:**
- Project title and 1–2 sentence overview
- Tech stack (table or list)
- Prerequisites (runtime versions if detectable from `.nvmrc`, `engines`, `go.mod`, etc.)
- Install / dev / test / build commands that exist in the repo
- Project structure (compact tree or directory map)
- License line if LICENSE file exists; otherwise omit or "TBD"

**README must not:**
- Duplicate entire AGENTS.md
- List every dependency
- Include secrets or `.env` values

### Step 5 — Write AGENTS.md

Target: **agents editing this repo** (Cursor, Codex, and other AGENTS.md-aware tools) — lean context always loaded. Keep **≤ 80 lines**. This is the **canonical** agent instruction file.

Use `~/.skills/init/templates/AGENTS.md.tpl` as outline.

**AGENTS.md must include:**
- What This Is (one short paragraph)
- Tech stack bullets
- Build & Run commands (copy from verified scripts)
- Project structure (key dirs only)
- Code style / testing conventions detected from samples
- Do Not Do (3–6 bullets: secrets, generated files, project-specific rules)

**AGENTS.md must not:**
- Repeat README marketing copy
- Exceed ~100 lines
- Store user preferences unrelated to this repo

Leave `## Current Goal` as an empty placeholder comment for the user to fill.

### Step 6 — Write CLAUDE.md

Target: **Claude Code**. Do **not** duplicate AGENTS.md content.

Default: write a thin import file using `~/.skills/init/templates/CLAUDE.md.tpl`:

```markdown
@AGENTS.md
```

Add Claude-specific notes below the import only when recon finds something Claude-only (rare). Prefer keeping all shared guidance in AGENTS.md.

If AGENTS.md is missing and the user asked for `--claude` only, still write the full lean agent body into AGENTS.md first (or ask), then point CLAUDE.md at it — avoid a standalone full CLAUDE.md that drifts.

### Step 7 — Verify

Before finishing:

```bash
test -f README.md && test -s README.md
test -f AGENTS.md && test -s AGENTS.md
test -f CLAUDE.md && test -s CLAUDE.md
wc -l AGENTS.md   # should be ≤ 100
```

Spot-check that every shell command in README/AGENTS appears in manifests, Makefile, or CI config. Remove or mark unverified commands.

Show the user:
- Which files were created vs updated
- Detected stack and commands
- Anything that could not be detected

---

## Output Examples

### Example 1 — Empty Next.js app

**User:** "Just created this Next app, no README yet"

**Action:** `/init` → detect `package.json`, `next.config.ts`, `src/app/` → write README + AGENTS + CLAUDE

**README:** install (`npm install`), dev (`npm run dev`), stack table, `src/app/` structure

**AGENTS:** commands, App Router layout, test command if present, do-not-do (don't edit `.next/`)

**CLAUDE:** `@AGENTS.md`

### Example 2 — README exists, AGENTS missing

**User:** "Add AGENTS.md for this Go service"

**Action:** `/init --agents` → read existing README for description → write AGENTS only; offer CLAUDE import if CLAUDE also missing

### Example 3 — All exist

**User:** `/init`

**Action:** Report all exist → ask whether to enhance specific sections or use `--force`

---

## Common Pitfalls

1. **Inventing npm scripts.** If `package.json` has no `test` script, don't write `npm test`.

2. **Overwriting a hand-written README.** Always read existing files; merge license, badges, deployment sections.

3. **AGENTS.md bloat.** Move architecture essays to README or a `docs/` file; keep AGENTS operational.

4. **Duplicating AGENTS into CLAUDE.** CLAUDE.md should import `@AGENTS.md`, not copy the body.

5. **Guessing stack from one import.** Require manifest or config confirmation before claiming a framework.

6. **Documenting ignored dirs.** Skip `node_modules/`, `.next/`, `dist/` in structure maps.

7. **Same content in README and AGENTS.** README = onboarding for humans; AGENTS = how to work in the repo as an agent.

---

## Verification Checklist

- [ ] Checked which of README.md / AGENTS.md / CLAUDE.md were missing before writing
- [ ] Ran `detect_project.py` or equivalent recon
- [ ] Every command in generated docs exists in the repo
- [ ] AGENTS.md ≤ 100 lines
- [ ] CLAUDE.md imports `@AGENTS.md` (no full duplicate body)
- [ ] No secrets, env values, or machine-specific paths without context
- [ ] User told what was created and what couldn't be detected
