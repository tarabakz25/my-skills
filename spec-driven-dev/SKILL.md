---
name: spec-driven-dev
description: "DEPRECATED — use /spec instead. Redirects to the unified spec skill for create, review, and build workflows."
version: 2.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spec, deprecated]
    related_skills: [spec]
---

# Spec-Driven Development (Deprecated)

This skill has been merged into **`/spec`**. Load `~/.skills/spec/SKILL.md` instead.

| Old workflow | New command |
|---|---|
| Spec creation | `/spec create <slug> [type]` |
| Spec review | `/spec review <spec-id>` |
| Implementation | `/spec build <spec-id>` |

Do not follow the old multi-skill pipeline (`/spec-creator` → `/spec-reviewer`). Use the unified skill.
