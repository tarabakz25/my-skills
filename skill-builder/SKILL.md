---
name: skill-builder
description: "Guide for building, structuring, and maintaining custom skills in ~/.skills/."
version: 1.0.0
author: Sumica
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, authoring, conventions, workflows, meta]
---

# Skill Builder

## Overview

Custom skills live under `~/.skills/<skill-name>/SKILL.md`. They are the agent's procedural memory — reusable approaches for recurring task types. A well-written skill makes the difference between guessing and knowing: it encodes exact commands, file paths, pitfalls, and verification steps so every session picks up where the last one left off.

This meta-skill documents how to build, organize, and maintain those custom skills.

## When to Use

**Use this skill when:**
- You need to create a new custom skill from scratch
- You're deciding whether something belongs as a skill vs. memory vs. a script
- You want to check the conventions for skill structure and frontmatter
- You're reviewing or refactoring an existing skill

**Don't use for:**
- One-shot tasks that won't recur (just use terminal directly)
- Environment facts that should go into `memory` (preferences, tool paths)
- Large standalone scripts (put those in `scripts/` within the skill directory)

## Skill vs. Memory vs. Script

| Artifact | When to Use | Example |
|----------|-------------|---------|
| **Skill** (`SKILL.md`) | Reusable workflow for a task category | "How to deploy a Minecraft server" |
| **Memory** (`memory` tool) | Durable facts, preferences, environment quirks | "User prefers bun over npm" |
| **Script** (`scripts/` in skill) | Automated logic with no agent reasoning needed | "Validate skill frontmatter" |

Rule of thumb: If a human would need to read instructions and think, it's a skill. If a machine can just run it, it's a script. If it's a fact that doesn't change, it's memory.

## Skill Directory Structure

Every custom skill lives in its own directory under `~/.skills/`:

```
~/.skills/
  <skill-name>/
    SKILL.md               # Required — the skill itself
    references/             # Optional — supporting docs, API references
      api.md
    templates/              # Optional — config templates, stubs
      config.yaml
    scripts/                # Optional — automation scripts referenced by SKILL.md
      validate.py
    assets/                 # Optional — images, diagrams
```

## Frontmatter Format

Every SKILL.md MUST start with frontmatter. This is the canonical format:

```yaml
---
name: my-skill-name               # lowercase with hyphens, max 64 chars
description: "Use when <trigger>. <one-line behavior>."  # max 1024 chars
version: 1.0.0
author: Sumica                     # your name/alias
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tag1, tag2, tag3]      # 2-5 descriptive tags
    related_skills: [other-skill]  # skills referenced within
---
```

**Rules:**
- `---` must be the very first bytes (no leading blank line or BOM)
- Closing `---` must be followed by a blank line before the body
- All YAML fields above are required
- `tags` and `related_skills` in `metadata.hermes` are strongly recommended

## SKILL.md Body Structure

After frontmatter, follow this structure:

```
# Title (same as name, but human-readable)

## Overview
2-3 paragraphs: what the skill does, why it exists, core philosophy.

## When to Use
- Bulleted list of trigger conditions
- "Don't use for:" section for counter-examples

## [Topic sections specific to the skill]
Exact commands, code blocks, file paths. Be specific — no placeholders.
Prefer numbered steps for sequential workflows.

## Common Pitfalls
Numbered list of mistakes the agent is likely to make, with fixes.

## Verification Checklist
- [ ] Post-action verification items
```

### Body Writing Rules

1. **Be complete.** Every command must be copy-pasteable. Every file path must be absolute or clearly relative.
2. **Assume zero context.** The agent reading this skill in a future session has no memory of your conversation. Write everything they need.
3. **No TODOs or placeholders.** If you write `TODO: fix this` in a skill, future-you will hit a wall. Finish content before saving.
4. **Prefer tables for reference data.** Quick-lookup tables beat prose for parameters, exit codes, config fields.
5. **Use code fences with language tags.** Syntax-highlighted and copyable.

## Workflow: Creating a New Skill

### Step 1: Identify the Trigger

Ask: "What recurring task category does this serve?" The trigger should be clear enough that the agent can load the skill automatically on the next matching request.

Good trigger: "Use when deploying a Python package to PyPI"
Bad trigger: "Use when doing Python stuff"

### Step 2: Survey Existing Skills

Check if something similar already exists:

```bash
ls ~/.skills/
```

If a skill covers 80% of what you need, extend it instead of creating a duplicate.

### Step 3: Draft the Skill

```bash
mkdir -p ~/.skills/<skill-name>
```

Write SKILL.md using the structure above. Include:
- Exact commands you ran (not generic versions)
- File paths that resolve on this machine
- Errors you hit and how you fixed them (these become Pitfalls)
- Verification steps that prove the workflow works

### Step 4: Validate

Check frontmatter integrity:

```python
import yaml, re, pathlib

content = pathlib.Path("~/.skills/<skill-name>/SKILL.md").expanduser().read_text()
assert content.startswith("---"), "Must start with ---"
m = re.search(r'\n---\s*\n', content[3:])
fm = yaml.safe_load(content[3:m.start()+3])
assert "name" in fm and "description" in fm
assert len(fm["name"]) <= 64
assert len(fm["description"]) <= 1024
assert len(content) <= 100_000
```

### Step 5: Add Supporting Files (if needed)

```bash
mkdir -p ~/.skills/<skill-name>/{references,templates,scripts,assets}
```

### Step 6: Commit to Version Control (Recommended)

```bash
cd ~/.skills
git init          # if not already a repo
git add <skill-name>/
git commit -m "skill: add <skill-name>"
```

## Naming Conventions

| Rule | Example |
|------|---------|
| lowercase with hyphens | `minecraft-server-deploy` |
| max 64 characters | Keep it short |
| describes the trigger, not the content | `pypi-publish` (not `pypi-publishing-guide`) |
| no abbreviations unless universal | `docker-compose` OK, `dc` not OK |

## Quality Checklist for Every Skill

- [ ] Frontmatter is valid (name, description, version, author, license, platforms, metadata)
- [ ] Description starts with "Use when ..." and is under 1024 chars
- [ ] `When to Use` section has both positive triggers and counter-examples
- [ ] Commands are exact (no fictional flags or paths)
- [ ] Pitfalls section captures real mistakes you've made
- [ ] Verification checklist proves the workflow works end-to-end
- [ ] Total content is under 100,000 chars (aim for 5-15k)
- [ ] No TODOs, placeholders, or unfinished sections

## Common Pitfalls

1. **Writing skills that are too generic.** "Use when writing Python" is too broad. "Use when setting up pytest with coverage" is specific enough to be actionable.

2. **Skipping the Pitfalls section.** This is the most valuable part of any skill — it saves future-you from repeating mistakes. Always include it.

3. **Hardcoding values that change.** Use template variables or reference config files instead of hardcoding paths like `/Users/kz/projects/foo` directly. If a path is stable, put it in `memory` and reference it from the skill.

4. **Writing overly long skills.** If a SKILL.md exceeds 20,000 chars, split detailed reference material into `references/*.md` and keep the SKILL.md focused on workflow.

5. **Forgetting verification steps.** Without verification, the agent can't tell if the task succeeded. Every step that produces output should have a "how to verify" line.

6. **Not committing the skill.** Skills in `~/.skills/` are ephemeral unless backed up. Initialize a git repo there and commit after each creation or significant update.

7. **Skill content that duplicates `memory`.** If a fact is about the user's preference or environment ("user prefers yarn over npm"), save it to `memory` (not the skill). Skills are for workflows, not user profiles.