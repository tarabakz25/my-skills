---
name: github-issue-creator
description: Create GitHub issues for the current repository with structured templates for bug reports and feature requests. Use when the user wants to report a bug, propose a feature, or create any GitHub issue ticket. Handles title generation, body formatting, label assignment, and milestone/assignee settings via the `gh` CLI.
disable-model-invocation: true
---

# GitHub Issue Creator

## Workflow

1. **Determine issue type** - Ask if not specified: `bug` or `feature`
2. **Gather information** - Ask only what's missing; infer from context when possible
3. **Draft the issue** - Show the user the title + body for confirmation before creating
4. **Create via `gh` CLI** - Use `gh issue create` with appropriate flags
5. **Output the issue URL**

## Creating Issues

### Commands

```bash
# Bug report
gh issue create \
  --title "<title>" \
  --body "<body>" \
  --label "bug,priority: high" \
  --assignee "@me"

# Feature request
gh issue create \
  --title "<title>" \
  --body "<body>" \
  --label "enhancement,priority: medium"

# List available labels (run first if unsure)
gh label list
```

### Title Format

- Bug: `fix: <component> - <what's broken>`  (例: `fix: ログイン画面 - パスワードリセットが動作しない`)
- Feature: `feat: <component> - <what to add>` (例: `feat: ダッシュボード - CSV エクスポート機能を追加`)

### Body Templates

See [templates.md](references/templates.md) for bug report and feature request templates.

## Label Strategy

Always apply at minimum:
- **Type**: `bug` or `enhancement`
- **Priority**: `priority: high` / `priority: medium` / `priority: low`

Optional:
- **Size**: `size: small` / `size: medium` / `size: large` (add when scope is estimable)
- `needs-triage` if not enough info to prioritize

If labels don't exist in the repo yet, create them first:
```bash
gh label create "priority: high" --color "D93F0B" --description "緊急度高"
gh label create "priority: medium" --color "FFA500" --description "通常優先度"
gh label create "priority: low" --color "0075CA" --description "優先度低"
```

## Priority Judgment

| Situation | Priority |
|-----------|----------|
| 本番クラッシュ・データ損失・セキュリティ | high |
| ユーザー体験を著しく損なう / 主要フローが壊れている | high |
| 一部機能が壊れているが回避策あり | medium |
| 軽微なUI不具合・小さな改善 | low |
| 新機能提案（緊急性なし） | low〜medium |

## Confirmation Step

Before running `gh issue create`, always show:
```
タイトル: <title>
ラベル: <labels>
本文:
---
<body>
---
作成しますか？ (y/n)
```

Wait for user confirmation before proceeding.
