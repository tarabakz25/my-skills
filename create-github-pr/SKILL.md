---
name: create-github-pr
description: Creates and opens a GitHub pull request from the current branch by summarizing git diff, drafting title/body, and submitting via gh CLI or GitHub MCP. Use when asked to create/open/submit a PR, このブランチでPRを作る, PRを出す, PR化する, or when branch changes need a reviewable GitHub PR.
disable-model-invocation: true
---

# Create GitHub PR

## Goal

Produce a reviewable PR scoped to `<base>...HEAD`, with accurate title/body, no duplicate PRs, and a clear outcome report (URL or blocker).

## Preconditions

- Repo + branch: `git rev-parse --show-toplevel`, `git branch --show-current`.
- Effective diff vs base: if empty, stop and say so.
- Auth:
  - Prefer `gh auth status` and `gh repo view`.
  - If `gh` is missing or blocked, use GitHub MCP (`user-github`): read tool schemas under the MCP descriptors, then call `create_pull_request` with `owner`, `repo`, `title`, `head`, `base`, optional `body`/`draft`.

## Base branch

Resolve in order:

1. User-specified base.
2. Default branch: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (or MCP equivalent).
3. Fallback: `main`, then `master`.

Use `git fetch --all --prune` when refs may be stale.

## Scope and hygiene

- `git log --oneline <base>..HEAD`
- `git diff --name-status <base>...HEAD` and `--stat`
- Uncommitted changes: do not silently mix into PR scope; commit or stash per user intent.
- Push: `git push -u origin HEAD` if no upstream.
- Duplicate check: `gh pr list --head <branch> --json url,number,state` (or `list_pull_requests` via MCP). If open PR exists, return that URL.

## Title and body

- Title: specific, intent-led (avoid "update files").
- Body: facts from diff and **only** checks actually run. Template: [references/pr-body-template.md](references/pr-body-template.md).
- Prefer writing body to a temp file and `gh pr create --body-file` to avoid shell escaping issues.

## Create PR

**Primary (non-interactive):**

```bash
gh pr create \
  --base "<base>" \
  --head "<branch>" \
  --title "<title>" \
  --body-file "<path-to-body.md>"
```

Optional: `--draft`, `--reviewer`, `--label` when requested.

**MCP fallback:** `create_pull_request` with same title/body/head/base; derive `owner`/`repo` from `gh repo view --json nameWithOwner` or `git remote get-url origin`.

## Report

Always include:

- PR URL (or existing PR URL)
- base / head
- 3–7 bullet summary of changes
- commands run for validation and outcomes (no invented CI results)

If blocked: exact error, minimal unblock steps, whether retry is idempotent.
