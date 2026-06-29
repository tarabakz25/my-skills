# PR Body Template

Use this template and fill only verified facts from the branch diff and executed checks.

```md
## Summary
- <What changed and why, in 1-3 bullets>

## Changes
- <Key implementation change>
- <Secondary change>
- <Any migration/config change>

## Impact
- <User-facing impact or "None">
- <Operational impact or "None">
- <Breaking change? Yes/No + detail>

## Validation
- [x] <Command actually run and result>
- [ ] <Not run: reason>

## Risks / Rollback
- Risk: <main risk>
- Rollback: <how to revert safely>
```

## Title Patterns

- `feat(<scope>): <new capability>`
- `fix(<scope>): <bug fix>`
- `refactor(<scope>): <internal change without behavior change>`
- `chore(<scope>): <maintenance>`

Prefer precise scope terms based on touched modules/directories.
