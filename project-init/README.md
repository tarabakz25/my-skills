# Project Init

Use when a new or existing project is missing README.md and/or CLAUDE.md. Analyzes the codebase and generates both from detected stack, commands, structure, and conventions.

## Usage

```
/project-init
/project-init --readme
/project-init --claude
```

## Scripts

```bash
python3 ~/.skills/project-init/scripts/detect_project.py .
```

## Related Skills

- [codebase-onboarding](../codebase-onboarding/SKILL.md) — deep architecture onboarding
- [prompt-optimizer](../prompt-optimizer/SKILL.md) — tune CLAUDE.md after generation
