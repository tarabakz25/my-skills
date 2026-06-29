---
name: create-pr-from-branch-diff
description: Create a pull request from the current Git branch diff against a base branch, including title/body drafting and PR creation via GitHub. Use when asked to "create PR", "open a PR", "ブランチ差分からPRを作る", "この変更をPR化して", or when branch-level code changes must be summarized and submitted as a reviewable PR.
---

# Create Pr From Branch Diff

## Overview

Create a high-quality pull request from the current branch by analyzing git diff and commit history, drafting a clear PR title/body, and opening the PR. Keep the PR scoped to actual branch changes and report the created PR URL with a concise change summary.

## Preconditions

- Confirm the current repository and branch with `git rev-parse --show-toplevel` and `git branch --show-current`.
- Confirm GitHub access:
  - Prefer `gh auth status` + `gh repo view`.
  - If `gh` is unavailable, use available GitHub MCP tools.
- Confirm there are commits or diff to submit. If no effective diff exists against base, stop and explain.

## Workflow

### 1) Identify base and review scope
- Resolve base branch in this order:
  1. User-specified base branch (if provided).
  2. Repository default branch (`gh repo view --json defaultBranchRef`).
  3. Fallback `main`, then `master`.
- Fetch latest refs when needed: `git fetch --all --prune`.
- Inspect scope:
  - `git log --oneline <base>..HEAD`
  - `git diff --name-status <base>...HEAD`
  - `git diff --stat <base>...HEAD`

### 2) Validate branch readiness
- Confirm clean intent:
  - If uncommitted changes exist, decide whether they should be committed before PR creation.
  - Never include unrelated local changes implicitly.
- Ensure branch exists on remote:
  - `git push -u origin HEAD` when upstream is missing.
- If checks are expected, run project-appropriate tests/lint before opening PR and include outcomes in PR body.

### 3) Draft PR title and body from diff
- Use commit intent + file-level impact to produce:
  - A specific title (avoid vague titles like "update files").
  - A body with context, key changes, risk, and validation.
- Keep claims evidence-based; do not invent test results.
- Use the template in [references/pr-body-template.md](references/pr-body-template.md).

### 4) Create PR
- Prefer non-interactive CLI:
```bash
gh pr create \
  --base <base-branch> \
  --head <current-branch> \
  --title "<pr-title>" \
  --body-file <path-to-body-md>
```
- Optional flags when requested: `--draft`, `--reviewer`, `--label`, `--milestone`.
- If a matching PR already exists, return that PR URL instead of creating duplicates (`gh pr list --head <branch>`).

### 5) Report outcome
- Return:
  - PR URL
  - base/head branches
  - concise summary of changes
  - test/lint status actually executed
- If blocked (auth/permission/no diff), report exact blocker and next command to unblock.

## Quality Bar

- Keep PR scope minimal and reviewable.
- Prefer explicit, reproducible commands over interactive steps.
- Include migration/ops notes when schema, infra, or env behavior changes.
- Call out breaking changes and rollback considerations clearly.

## Quick Command Set

```bash
# Current context
git branch --show-current
git status --short
gh repo view --json nameWithOwner,defaultBranchRef

# Diff summary against base
git log --oneline <base>..HEAD
git diff --name-status <base>...HEAD
git diff --stat <base>...HEAD

# Push branch if needed
git push -u origin HEAD

# Create PR
gh pr create --base <base> --head <branch> --title "<title>" --body-file <body.md>
```

## Output Contract

- Provide one final response containing:
  - PR URL
  - title
  - base/head
  - change summary (3-7 bullets)
  - verification run and results
- If PR was not created, provide:
  - root cause
  - exact command(s) to resolve
  - whether retry is safe/idempotent
