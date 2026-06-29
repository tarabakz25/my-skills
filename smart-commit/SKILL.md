---
name: smart-commit
description: Analyzes git diff and automatically creates commits with Conventional Commits format messages. Use when the user wants to commit changes, mentions "smart commit", or asks to analyze changes and commit them automatically.
---

# Smart Commit

This skill automatically analyzes git changes and creates commits with well-formatted Conventional Commits messages.

## When to Use

- User asks to commit changes
- User mentions "smart commit" or similar phrases
- User wants automatic commit message generation based on diff analysis
- User requests to analyze and commit changes

## Instructions

Follow these steps in order:

### 1. Check Repository Status

First, verify this is a git repository and check current status:

```bash
git status
```

If not a git repository, inform the user and exit.

### 2. Analyze Changes

Get both staged and unstaged changes:

```bash
git diff
git diff --cached
```

If no changes exist, inform the user and exit.

### 3. Stage All Changes

Automatically stage all changes:

```bash
git add -A
```

### 4. Analyze Diff and Generate Commit Message

Examine the staged diff carefully:

```bash
git diff --cached
```

Based on the changes, generate a commit message following **Conventional Commits** format:

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Build process, tools, dependencies
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes
- `revert`: Reverting previous commits

**Guidelines**:
- Scope is optional but recommended (e.g., `auth`, `api`, `ui`)
- Subject should be concise, in imperative mood
- If multiple unrelated changes exist, mention the most significant one
- Keep the message under 72 characters for the first line
- Use lowercase for subject (except proper nouns)
- No period at the end of subject

**Examples**:
- `feat(auth): add JWT token validation`
- `fix(api): resolve null pointer in user endpoint`
- `docs(readme): update installation instructions`
- `refactor(database): simplify query builder logic`
- `test(user): add unit tests for login function`

### 5. Execute Commit

Create the commit with the generated message:

```bash
git commit -m "<generated-message>"
```

**Important**:
- Do NOT add Claude Code attribution footer (no "Generated with Claude Code" or "Co-Authored-By")
- Keep the message clean and professional
- Use only the Conventional Commits format

### 6. Confirm Success

After committing, show:
1. The commit message used
2. Summary of what was committed
3. Current git status

## Error Handling

- **No git repository**: Inform user and suggest `git init`
- **No changes**: Inform user that working directory is clean
- **Commit fails**: Show error message and suggest fixes

## Examples

### Example 1: Feature Addition

**Changes**: Added new login page component

**Generated Message**: `feat(auth): add login page component`

### Example 2: Bug Fix

**Changes**: Fixed null pointer exception in API handler

**Generated Message**: `fix(api): resolve null pointer in request handler`

### Example 3: Multiple Files

**Changes**: Updated README.md and added installation script

**Generated Message**: `docs(project): add installation script and update readme`

### Example 4: Refactoring

**Changes**: Reorganized database query logic

**Generated Message**: `refactor(db): reorganize query builder structure`

## Notes

- This skill operates fully automatically without user confirmation
- All unstaged and staged changes will be included
- The skill focuses on creating meaningful, concise commit messages
- Conventional Commits format ensures consistency across the project
