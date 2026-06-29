# Codebase Deck Patterns

Use this reference when turning repository findings into a slide structure.

## Common Deck Structures

### Architecture overview

1. Title: system name and one-sentence purpose.
2. Why it exists: user/business problem and operating context.
3. System map: major components and external dependencies.
4. Request or data flow: one representative end-to-end journey.
5. Key design choices: boundaries, abstractions, tradeoffs.
6. Operational shape: build, deploy, config, observability, risks.
7. Next steps: open questions, improvement areas, or recommended actions.

### Onboarding walkthrough

1. What this repo does.
2. How the code is organized.
3. How to run and test it.
4. Main workflow walkthrough.
5. Where common changes live.
6. Testing and release guardrails.
7. First tasks or learning path.

### Feature deep dive

1. Feature promise and user journey.
2. Entry points and routing/API surface.
3. State/data model.
4. Core service flow.
5. Edge cases and error handling.
6. Test coverage and gaps.
7. Extension or refactor recommendations.

### Refactor proposal

1. Current state and user/developer pain.
2. Evidence from code: duplication, coupling, risk, slow path, or bug history.
3. Target shape.
4. Option comparison.
5. Recommended plan.
6. Migration phases and compatibility.
7. Validation and rollback.

## Visual Forms

- Module map: boxes only when they represent real packages, services, or runtime boundaries.
- Sequence flow: user/client -> route/controller -> service -> data/external dependency -> response.
- Data model: entities, key fields, relationships, ownership, lifecycle.
- Responsibility matrix: module vs responsibility, with clear ownership and gaps.
- Before/after: current flow and target flow, using the same visual grammar.
- Risk map: likelihood/impact or path-to-failure, tied to source evidence.
- Annotated snippet: 5-15 lines max, with two or three callouts.

## Evidence Notes

Prefer source paths that a maintainer can open immediately:

```text
src/server/routes/users.ts: creates user-facing API boundary
prisma/schema.prisma: owns account and subscription relationships
tests/billing.test.ts: documents retry and idempotency behavior
```

Use line numbers when the deck depends on a specific implementation detail. Use file-level references when the slide discusses broader ownership or structure.

## Language And Tone

For Japanese decks, keep slide text concise and natural:

- Use short noun phrases for titles.
- Avoid literal translations of internal identifiers when they are clearer as code terms.
- Put long explanations in speaker notes.
- Keep file paths and symbols in monospace where the slide tool supports it.

For executive or non-engineer audiences, reduce framework names and implementation mechanics. Keep only the technical details needed to support decisions.
