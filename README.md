# Skills Library

A consolidated collection of agent skills for Claude, Cursor, and Codex — procedural memory encoded as Markdown workflows.

## Overview

This repository holds **~33 skills** under `~/.skills/`, merged from `~/.claude/skills/`, `~/.cursor/skills/`, and `~/.codex/skills/`. Each skill is a self-contained directory with a `SKILL.md` file that tells agents how to handle a specific task category (deployment, spec writing, code review, etc.).

Skills are not a runnable application. Agents load them on demand when a task matches the skill's trigger conditions.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Skill format | Markdown + YAML frontmatter |
| Optional scripts | Python, shell (per-skill) |
| System skills | `.system/` (Codex preinstalled skills) |

## Getting Started

### Prerequisites

- A compatible agent runtime (Claude Code, Cursor, Codex, etc.) configured to read from `~/.skills/`
- For editing skills: any text editor
- For skills with bundled tests: Python 3.11+ and `pytest`

### Install

No install step at the repo level. Skills are consumed directly from this directory. Agent runtimes typically symlink or copy skills into their own paths (e.g. `~/.claude/skills/`, `~/.cursor/skills/`, `~/.codex/skills/`).

To scaffold project docs in any repo:

```bash
python3 ~/.skills/init/scripts/detect_project.py .
```

### Per-Skill Tests

Only individual skills define tests; run them inside the skill directory that defines them. There is no root-level test or build command.

## Project Structure

```
~/.skills/
├── init/                  # Generate README.md / AGENTS.md / CLAUDE.md for other projects
├── make-skill/            # Meta-skill: create or update skills
├── solo-sdd/              # Lightweight solo SDD workflow
├── code-review/           # Example domain skill
├── .system/               # Codex system skills (imagegen, skill-installer, etc.)
└── <skill-name>/          # One directory per skill
    ├── SKILL.md           # Required — the skill itself
    ├── references/        # Optional supporting docs
    ├── templates/         # Optional stubs
    ├── scripts/           # Optional automation
    └── tests/             # Optional (rare, per-skill)
```

## Authoring Skills

Read `make-skill/SKILL.md` before creating or editing skills (`/make-skill`). Conventions:

- Directory name: lowercase kebab-case (`my-skill-name/`)
- Required frontmatter: `name`, `description`, `version`, `author`, `license`, `platforms`, `metadata.hermes`
- Body sections: Overview, When to Use, workflow sections, Common Pitfalls, Verification Checklist

To init docs for a new codebase project:

```
/init
```

See `init/SKILL.md` for flags (`--readme`, `--agents`, `--claude`, `--force`).

## License

Individual skills declare their own license in frontmatter (typically MIT). No root LICENSE file.
