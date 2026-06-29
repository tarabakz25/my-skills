# PR body template

Fill only verified facts from the branch diff and executed checks.

```md
## Summary
- <What changed and why, 1–3 bullets>

## Changes
- <Primary change>
- <Secondary change>
- <Config/migration note if any>

## Impact
- <User-facing or "None">
- <Operational or "None">
- <Breaking change? Yes/No + detail>

## Validation
- [x] <Command run + result>
- [ ] <Not run + reason>

## Risks / Rollback
- Risk: <main risk>
- Rollback: <safe revert path>
```

## Title patterns

- `feat(<scope>): …`
- `fix(<scope>): …`
- `refactor(<scope>): …`
- `chore(<scope>): …`

Use scope from touched areas (dirs/modules).
