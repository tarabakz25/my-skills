---
name: smart-commit
description: Analyze git diff, compare scope with the previous commit, and split staging into separate Conventional Commits when different scopes are mixed. Use when the user wants to commit changes, mentions "smart commit", asks for scoped/split commits, or wants unrelated changes committed separately.
disable-model-invocation: true
---

# Smart Commit

This skill analyzes changes, compares them with the most recent commit scope, and creates separate commits per scope instead of committing everything at once.

## When to Use

- User asks to commit changes or mentions "smart commit"
- User wants automatic commit message generation based on diff analysis
- User asks for automatic commit with scope-aware splitting
- User wants unrelated changes committed separately
- User wants staging decisions based on diff contents
- User asks to avoid mixing different concerns in one commit

## Core Policy

- Do not stage all files blindly.
- Split changes into coherent scope groups.
- If a scope differs from the previous commit scope, create a separate staged set and separate commit.
- Keep Conventional Commits format for each commit message.

## Instructions

Follow these steps in order:

### 1. Inspect repository and current state

```bash
git status --short
git diff --name-status
git diff --cached --name-status
```

If there are no changes, report and exit. If this is not a git repository, inform the user and suggest `git init`.

### 2. Detect the previous commit scope

Read previous subject and touched paths:

```bash
git log -1 --pretty=%s
git show --name-only --pretty="" HEAD
```

Determine `previous_scope` as follows:

1. If subject matches `<type>(<scope>): ...`, use that `<scope>`.
2. Otherwise infer from dominant path area in previous commit.
3. If still unclear, set `previous_scope=unknown` and continue with path-based grouping only.

### 3. Classify current changes into scope groups

Use file paths and diff intent to classify each change.

Recommended heuristics:

- `docs/**`, `README*`, `*.md` -> `docs`
- `test/**`, `__tests__/**`, `*.test.*`, `*.spec.*` -> `test`
- `ci/**`, `.github/workflows/**` -> `ci`
- `scripts/**`, tooling config files -> `chore`
- `src/<domain>/**` -> `<domain>` (e.g. `auth`, `api`, `ui`, `db`)

If a single file contains mixed concerns, split hunks with:

```bash
git add -p <file>
```

### 4. Build staging sets by scope

Create separate staging sets per scope and commit each set independently.

Important rules:

- If one scope matches `previous_scope`, it may be committed first as a continuation.
- Every scope different from `previous_scope` must be committed separately.
- Never include unrelated scope files in the same commit.

Use selective staging:

```bash
git add <files-of-one-scope>
git diff --cached --name-only
```

If incorrect files were staged:

```bash
git restore --staged <file>
```

### 5. Generate one commit message per scope

For each staged set, generate Conventional Commit message:

Format: `<type>(<scope>): <subject>`

Type decision hints:

- `feat`: new behavior
- `fix`: bug correction
- `refactor`: structural change, no behavior change
- `docs`: documentation
- `test`: test changes
- `style`: formatting only, no logic change
- `chore`: maintenance/tooling
- `perf`: performance improvements
- `ci`: CI/CD changes
- `build`: build system changes
- `revert`: reverting previous commits

Keep subject concise, imperative, lowercase where reasonable, under 72 characters, no trailing period.

### 6. Commit in sequence

For each scope group:

```bash
git commit -m "<generated-message>"
```

Repeat until all groups are committed.

### 7. Final verification

```bash
git log --oneline -n 5
git status --short
```

Report:

1. Created commits (newest first)
2. Files included in each commit
3. Remaining uncommitted changes (if any)

## Safety Rules

- Do not use `git add -A` by default.
- Do not rewrite history (`rebase`, `reset --hard`) unless explicitly requested.
- If classification is ambiguous, use the smallest safe commit boundaries and explain assumptions.
- If a commit fails, show the error and suggest fixes; do not force through hooks.

## Example Outcome

- Previous commit: `feat(auth): add refresh token endpoint`
- Current changes include:
  - `src/auth/*` bug fix
  - `docs/api.md` update
  - `.github/workflows/ci.yml` adjustment

Expected split:

1. `fix(auth): handle expired refresh token error`
2. `docs(api): update token refresh documentation`
3. `ci(workflows): refine ci job conditions`

## Notes

- This skill operates fully automatically without user confirmation
- Changes are grouped by scope; unrelated concerns are never mixed in one commit
- Conventional Commits format ensures consistency across the project
