---
name: patch
description: >-
  Ships a lightweight fix or improvement as a short-lived patch branch and
  opens one PR with the solo-sdd PR body shape. Use for /patch, quick fix,
  small improvement, hotfix-lite, or when the change is too small for
  solo-sdd and should not land on staging or other long-lived dedicated
  branches.
disable-model-invocation: true
version: 1.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [patch, hotfix, quick-fix, pr, lightweight, improvement]
    related_skills: [solo-sdd, create-github-pr, smart-commit, code-review]
---

# Patch

## Overview

Make a **small, reviewable** fix or improvement on a short-lived branch, then open **one PR**. No `.sdd/` brief/design, no worktree ceremony.

Default: branch from the repo **default branch** as `patch/{slug}`, commit, PR into that default (or user-specified base).

## When to Use

**Use when:**
- User invokes `/patch`, asks for a quick fix / small improvement / lightweight PR
- Scope is obvious and small (typo, config tweak, tiny bugfix, narrow polish)
- Work should **not** go on `staging`, `release/*`, or other long-lived dedicated branches

**Don't use for:**
- Features that need intent pinning → `solo-sdd`
- Large refactors, multi-file redesigns, or unclear product decisions
- Already on a dedicated long-lived branch where the change belongs in that track (ask; do not invent a parallel patch PR)

## Branch policy

**Dedicated / long-lived branches (do not patch on top):**  
`staging`, `stage`, `release`, `release/*`, `prod`, `production`, `develop` (when used as integration), and any branch the user or repo treats as a permanent integration line.

| Current branch | Action |
|----------------|--------|
| Dedicated (above) | Stop. Explain. Ask: leave the change for that track, or start a `patch/*` from default instead. |
| Default (`main` / `master` / repo default) | Create `patch/{slug}` from up-to-date default. |
| Existing `patch/*` (or user-named short-lived branch) | Reuse if it matches this patch; else ask. |
| Other feature branch | Ask once: continue here vs new `patch/*` from default. Default preference: new `patch/*` from default so the PR stays minimal. |

```bash
git fetch --all --prune
DEFAULT=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
# fallback: main, then master
git switch -c "patch/${SLUG}" "origin/${DEFAULT}"
```

`{slug}`: short kebab-case English (e.g. `cookie-secure-flag`, `readme-typo`).

## Workflow

```
Progress:
- [ ] 1. Scope check (lightweight? not on dedicated branch?)
- [ ] 2. Branch from default → patch/{slug}
- [ ] 3. Implement + verify (minimal diff)
- [ ] 4. Open PR (solo-sdd body shape)
- [ ] 5. Report URL
```

### 1) Scope check

- Confirm the ask is a **light** patch (prefer one concern; avoid drive-by cleanup).
- If it needs design / multi-task tracking → redirect to `solo-sdd`.
- Resolve current branch; apply [Branch policy](#branch-policy).

### 2) Branch

- Fetch; create or reuse `patch/{slug}` from default (unless user explicitly names another short-lived branch / base).
- Keep the working tree focused: do not mix unrelated local changes into the patch.

### 3) Implement and commit

- Change only what the patch needs.
- Commit with a clear message (Conventional Commits if the repo uses them). Prefer `smart-commit` when scopes are mixed.
- Do not invent tests; run project-appropriate checks when cheap and relevant. Record only what actually ran.

### 4) Open PR

Push and open **one** PR into **base** (default branch unless user specifies otherwise). Prefer `gh pr create` / `create-github-pr` mechanics (auth, duplicate check, `--body-file`).

**Title** (same pattern as solo-sdd): `{GENRE}: {feature}` — `GENRE` uppercase (`FIX`, `CHORE`, `PERF`, …); `{feature}` short English phrase.

Examples: `FIX: session cookie race`, `CHORE: typo in deploy docs`

**Body:** use this template **verbatim** (same headings, same order). Canonical copy: [references/pr-template.md](references/pr-template.md) (aligned with [solo-sdd/references/pr-template.md](../solo-sdd/references/pr-template.md); Spec filled for no-`.sdd` patches).

```markdown
## Summary

### What

- ...

### Why

- ...

### Spec

- None (lightweight patch; no `.sdd/` brief/design)

## Test

### How to test

- [ ] ...

### Captures

- ...

## Deploy Notes

- None
```

**PR body rules:**
- **What**: what changed, 1–3 bullets
- **Why**: motivation (bug / friction / small win)
- **Spec**: always the no-`.sdd` line above for this skill (do not invent fake brief/design links). If the user later points at real docs, link those instead under Spec.
- **How to test**: concrete steps; check only what was actually run
- **Captures**: screenshots / logs / command output, or `None`
- **Deploy Notes**: env, migration, flag, or ops follow-up — or `None`
- Prefer temp file + `gh pr create --body-file`

```bash
git push -u origin HEAD
gh pr create --base "${BASE}" --title "${GENRE}: ${FEATURE_EN}" --body-file /tmp/patch-pr-body.md
```

If an open PR already exists for this head, return that URL (no duplicate).

### 5) Report

- PR URL
- base / head
- 1–5 bullet summary
- checks actually run

No mandatory worktree close step (unlike solo-sdd). Leave local `patch/*` unless the user asks to delete it.

## Common pitfalls

- Using this on `staging` / release lines without asking
- Growing a “tiny” patch into a feature (stop; switch to `solo-sdd`)
- Fake Spec links to non-existent `.sdd/` paths
- Invented test/CI results in the PR body
- Broad drive-by refactors in the same PR

## Verification checklist

- [ ] Not committed on a dedicated long-lived branch without explicit user choice
- [ ] Branch is short-lived (`patch/{slug}` or user-named equivalent)
- [ ] Diff is minimal and single-concern
- [ ] Title `{GENRE}: {feature}`; body uses verbatim PR headings
- [ ] Spec uses no-`.sdd` line (or real docs only if user provided them)
- [ ] PR URL reported; no duplicate PR created
