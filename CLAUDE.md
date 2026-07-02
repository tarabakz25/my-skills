# Skills Library

## What This Is

Consolidated agent skill library at `~/.skills/`. ~33 skills from Claude, Cursor, and Codex sources. Each skill is `<skill-name>/SKILL.md` — a Markdown workflow with YAML frontmatter that agents load when a task matches.

## Tech Stack

- Markdown + YAML frontmatter (`SKILL.md`)
- Optional Python/shell scripts inside skill directories
- `.system/` — Codex system skills (preinstalled; rarely edit)

## Build & Run

No repo-level build, dev, or lint commands. This is a content library, not an application.

Per-skill recon helper:

```bash
python3 ~/.skills/project-init/scripts/detect_project.py .
```

## Project Structure

- `SKILL.md` — one per skill directory; the only required file
- `references/`, `templates/`, `scripts/`, `assets/` — optional per skill
- `skill-builder/` — authoring conventions (read before creating skills)
- `project-init/` — generate README/CLAUDE for other repos
- `spec/` — spec-driven dev (`/spec create|review|build`)

## Code Style

- Skill directory names: lowercase kebab-case
- Frontmatter must start at byte 0 with `---`; required fields per `skill-builder/SKILL.md`
- Body: Overview → When to Use → workflow sections → Common Pitfalls → Verification Checklist
- Commands and paths must be copy-pasteable; no TODO placeholders in committed skills
- Prefer extending an existing skill over duplicating (~80% overlap rule)

## Testing

- No root test suite
- Some skills may bundle their own tests
- Run tests only inside the skill directory that defines them

## Conventions

- Source priority when merging duplicates: `.claude` > `.cursor` > `.codex`
- Tags and `related_skills` in `metadata.hermes` are strongly recommended

## Do Not Do

- Do not invent npm/build commands — this repo has no `package.json`
- Do not bulk-edit skills without reading each `SKILL.md` first
- Do not commit secrets, tokens, or machine-specific credentials
- Do not overwrite user-written README/CLAUDE in other projects without reading and merging
- Do not treat `.system/` skills as ordinary custom skills unless explicitly asked
- Do not add root-level tooling (package.json, Makefile) without user request

## Current Goal

<!-- Update when starting focused work -->
