---
name: spec-driven-dev
description: "Use when starting feature development, API design, or system changes that require explicit requirements alignment. Orchestrates the full spec-driven workflow: spec creation → review → plan → TDD implementation → spec compliance verification. Treats the spec as the single source of truth throughout."
version: 1.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spec, tdd, workflow, requirements, development]
    related_skills: [spec-creator, spec-reviewer, tdd-workflow, verification-loop, blueprint]
---

# Spec-Driven Development

## Overview

Spec-driven development (SDD) is a workflow where a written spec — not the code, not the tests, not informal conversation — is the definitive statement of what to build. Every implementation decision traces back to a spec item. Every ambiguity gets resolved in the spec before writing code.

This skill orchestrates the full pipeline: spec creation, review, plan derivation, TDD implementation, and compliance verification. It leans on `/spec-creator`, `/spec-reviewer`, and `/tdd-workflow` for their respective phases and adds the traceability layer and compliance gate that tie them together.

The key invariant: **if it isn't in the spec, don't build it; if it's in the spec, prove it's built.**

## When to Use

**Use this skill when:**
- Starting a new feature where requirements need to be pinned down before coding
- Building an API or data model where multiple consumers need alignment
- Working on a change large enough that informal task descriptions would cause drift
- Doing any development where a reviewer or stakeholder needs to sign off on what's being built

**Don't use for:**
- One-line bug fixes with an obvious and agreed-upon correct behavior
- Purely exploratory spikes (write a spike-spec separately when done)
- Pure refactors with zero behavior change (the existing tests are the spec)

## Core Concept: Spec Item IDs

Every requirement in the spec gets a unique ID in the format `SPEC-NNN`. These IDs are the traceability mechanism — they appear in:

- Spec document section headers and bullet points
- Test names: `test("SPEC-042: rejects negative amounts")`
- Commit messages: `feat: add payment validation [SPEC-042, SPEC-043]`
- PR descriptions: "Closes SPEC-041 through SPEC-044"

This makes the compliance check mechanical: grep for unimplemented IDs.

## Workflow

### Phase 1: Spec Creation

Invoke `/spec-creator` to generate the spec. Save it to `specs/todo/YYYYMMDD-<feature-slug>.md` (use today's date).

After the draft is generated:
1. Add a `## Spec Items` section at the bottom with a numbered list of all testable requirements extracted from the document, each with a `SPEC-NNN` ID.
2. Number sequentially from `SPEC-001` (or continue from the last used ID if other specs exist in the project).

**Spec Items section format:**
```markdown
## Spec Items

| ID | Requirement | Priority |
|----|-------------|----------|
| SPEC-001 | User can create a payment with a positive amount | P0 |
| SPEC-002 | System rejects payments with amount ≤ 0 | P0 |
| SPEC-003 | Payment confirmation email sent within 5s of creation | P1 |
```

Priority:
- `P0` — must be implemented before any merge
- `P1` — required for the feature to be considered complete
- `P2` — nice to have, can be deferred

### Phase 2: Spec Review

Invoke `/spec-reviewer` with the generated spec as input.

Critical: **do not write any code until P0 and P1 issues from the review are resolved.** Update the spec to address each 🔴 Critical and 🟡 Major finding. If a finding changes or removes a SPEC item, update the Spec Items table accordingly.

Mark the spec as reviewed by adding to the frontmatter (if YAML) or the top of the document:

```
Reviewed: true
Review date: YYYY-MM-DD
Open issues: none / <count>
```

### Phase 3: Plan Derivation

Derive the implementation plan directly from the Spec Items table. Group items by component or layer (e.g., data model, API, business logic, UI). For each group:

1. List the SPEC IDs it covers
2. List files to create or modify
3. Estimate complexity (S/M/L)

**Do not add tasks that have no corresponding SPEC ID.** If you find something that needs doing but isn't in the spec, either add a new SPEC item first or flag it as out-of-scope.

```
Implementation Plan
===================
Group 1: Data model [SPEC-001, SPEC-002]
  - Create src/models/payment.ts
  - Add migration: 20240617_add_payments_table.sql
  Complexity: S

Group 2: Validation logic [SPEC-002, SPEC-004]
  - Create src/validators/payment.ts
  Complexity: S

Group 3: API endpoint [SPEC-001, SPEC-003, SPEC-005]
  - Modify src/routes/payments.ts
  Complexity: M
```

### Phase 4: TDD Implementation

Follow `/tdd-workflow` for each implementation group. The additional constraint for SDD:

**Every test must reference its SPEC ID in the test name:**

```typescript
// Good
it("SPEC-002: rejects payment when amount is zero", () => { ... })
it("SPEC-002: rejects payment when amount is negative", () => { ... })

// Bad — no traceability
it("validates payment amount", () => { ... })
```

When writing a test for a behavior not covered by any SPEC ID, stop and either:
- Add the missing requirement to the spec with a new SPEC ID
- Confirm it's an implementation detail not requiring a spec item (e.g., internal helper behavior)

### Phase 5: Spec Compliance Verification

After all P0/P1 items are implemented, run the compliance check:

```bash
# List all SPEC IDs in the spec
grep -oE 'SPEC-[0-9]+' specs/{todo,inprogress,done}/<feature-name>.md | sort -u

# List all SPEC IDs referenced in tests
grep -rE 'SPEC-[0-9]+' src/ tests/ | grep -oE 'SPEC-[0-9]+' | sort -u

# Find SPEC IDs in spec but not in tests (unimplemented)
comm -23 \
  <(grep -oE 'SPEC-[0-9]+' specs/{todo,inprogress,done}/<feature-name>.md | sort -u) \
  <(grep -rE 'SPEC-[0-9]+' src/ tests/ | grep -oE 'SPEC-[0-9]+' | sort -u)
```

**The output of the last command must be empty for P0 items before merging.** P1 items should also be empty unless explicitly deferred with a written justification.

If `/verification-loop` is available, invoke it with the spec path as the target document for a semantic compliance pass in addition to the grep-based check.

### Phase 6: Update or Close the Spec

After merge:
- Move the file: `git mv specs/inprogress/YYYYMMDD-<feature>.md specs/done/`
- Update `Status: done` in the spec header
- If the feature has ongoing evolution, keep the spec in `done/` as living documentation; move back to `inprogress/` before implementing any change

## Spec Document Location and Naming

### File name format

```
YYYYMMDD-<feature-slug>.md
```

Examples: `20260617-payment-creation.md`, `20260618-payments-api.md`

- Date = the day the spec is first created (not the implementation date)
- `feature-slug` = lowercase, hyphens, no spaces, no version numbers

### Directory layout

Specs live under `specs/` at the project root, split into three lifecycle subdirectories:

```
project-root/
  specs/
    todo/          # Spec written, not yet being implemented
    inprogress/    # Actively being implemented
    done/          # Implementation merged and verified
```

Never create subdirectories other than `todo/`, `inprogress/`, `done/`. Never put specs inside `src/` or `docs/`.

### Lifecycle transitions

Move the file (not copy) when status changes:

```bash
# Start implementation
git mv specs/todo/20260617-payment-creation.md specs/inprogress/

# Implementation complete and merged
git mv specs/inprogress/20260617-payment-creation.md specs/done/
```

Always commit the move as a standalone commit:
```
git commit -m "spec: move payment-creation to inprogress"
```

Update the `Status:` field in the spec header to match the directory:
- `todo/` → `Status: todo`
- `inprogress/` → `Status: inprogress`
- `done/` → `Status: done`

### Bootstrap (first spec in a project)

```bash
mkdir -p specs/todo specs/inprogress specs/done
touch specs/todo/$(date +%Y%m%d)-<feature-slug>.md
```

## Handling Spec Changes During Implementation

When requirements change after coding has started:

1. **Update the spec first** — change the spec document, update or add SPEC IDs
2. **Update affected tests** — tests referencing the changed SPEC ID must be updated to match the new requirement
3. **Then update the implementation** — code follows tests, tests follow spec
4. **Never update the code first** — this inverts the dependency and makes the spec a lie

If a stakeholder asks for a change verbally or in a ticket, refuse to code it until it's reflected in the spec. "Can you just make it do X?" → "I'll update the spec first, takes 5 minutes."

## Common Pitfalls

1. **Writing SPEC IDs after the fact.** Retrofitting IDs to existing tests defeats the purpose — it adds bureaucracy without traceability. IDs must be assigned before writing the tests.

2. **Treating vague spec language as good enough.** "The system should handle errors gracefully" is not a SPEC item. It becomes one only when it says: "SPEC-007: API returns HTTP 422 with `{error: string}` body when validation fails."

3. **Skipping the review phase under time pressure.** The review phase exists precisely for time-pressured situations — catching ambiguities before coding is 10× cheaper than discovering them during review or post-deploy.

4. **Implementing beyond the spec.** If you add behavior not in the spec, it has no test coverage mandate and no review. Either add it to the spec or don't build it.

5. **Letting the spec drift from reality.** A spec that no longer matches the code is worse than no spec — it actively misleads. Update the spec whenever behavior changes, even for "small" things.

6. **One giant spec for a large system.** Split into focused per-feature or per-domain specs. A spec over 500 lines is hard to review effectively. Reference other specs with `See: spec/payments-api.md`.

7. **Confusing spec items with implementation tasks.** `SPEC-001: user can create a payment` is a requirement. "Create Payment model class" is a task. Tasks belong in the implementation plan, not the Spec Items table.

## Verification Checklist

- [ ] `specs/todo/YYYYMMDD-<feature>.md` exists with correct naming format
- [ ] File moved to `specs/inprogress/` before implementation starts
- [ ] Spec header has `Status:` matching the current directory
- [ ] Spec Items table complete — all testable requirements have a `SPEC-NNN` ID
- [ ] P0/P1 spec review findings resolved (no open 🔴 Critical)
- [ ] Implementation plan maps every task to at least one SPEC ID
- [ ] All tests include `SPEC-NNN` in the test name
- [ ] Compliance grep returns no unimplemented P0 IDs
- [ ] Compliance grep returns no unimplemented P1 IDs (or deferrals are documented)
- [ ] Spec marked `Status: Implemented` after merge
