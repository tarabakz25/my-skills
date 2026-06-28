---
name: spec
description: "Use when creating, reviewing, or implementing from specification documents. Unified spec-driven workflow via /spec create, /spec review {spec-id}, and /spec build {spec-id}. Treats the spec as single source of truth with SPEC-NNN traceability through TDD implementation."
version: 2.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spec, sdd, tdd, requirements, review, build]
    related_skills: [tdd-workflow, verification-loop, blueprint, code-review]
---

# Spec

## Overview

Spec-driven development (SDD) treats a written spec — not code, not informal conversation — as the definitive statement of what to build. This skill consolidates spec **creation**, **review**, and **implementation** into one command surface.

The key invariant: **if it isn't in the spec, don't build it; if it's in the spec, prove it's built.**

Every requirement gets a `SPEC-NNN` ID for traceability through tests, commits, and compliance checks.

## When to Use

**Use this skill when:**
- User invokes `/spec`, `/spec create`, `/spec review {spec-id}`, or `/spec build {spec-id}`
- User asks to "create a spec", "review the spec", "implement from spec", or "spec-driven development"
- Starting a feature where requirements must be pinned before coding
- Building APIs or data models where multiple consumers need alignment

**Don't use for:**
- One-line bug fixes with obvious correct behavior
- Purely exploratory spikes (write a spike-spec when done)
- Pure refactors with zero behavior change (existing tests are the spec)

## Command Interface

Parse the user's first token after `/spec` as the subcommand.

| Command | Action |
|---------|--------|
| `/spec` | Show help + list all specs in `specs/` |
| `/spec create <slug> [type]` | Create a new spec draft |
| `/spec review <spec-id>` | Review an existing spec (3-round review) |
| `/spec build <spec-id>` | Implement from a reviewed spec (plan → TDD → compliance) |

**Arguments:**
- `<slug>` — lowercase kebab-case feature name (e.g., `payment-creation`)
- `<spec-id>` — full filename stem (`20260617-payment-creation`) or unique slug suffix (`payment-creation`)
- `[type]` — optional spec type: `feature` (default), `api`, `system`, `data`

### Resolve spec-id to file path

Always resolve before `review` or `build`:

```bash
# From project root — returns first match or empty
find specs/todo specs/inprogress specs/done -name "*${SPEC_ID}*.md" 2>/dev/null | head -1
```

If zero matches: report "spec not found" and list available specs.
If multiple matches: ask user to disambiguate with full date prefix.

### List available specs

```bash
find specs/todo specs/inprogress specs/done -name '*.md' 2>/dev/null \
  | sort \
  | while read f; do
      basename "$f" .md
      grep -m1 '^Status:' "$f" 2>/dev/null || echo "  (no Status field)"
    done
```

---

## `/spec create <slug> [type]`

Create a specification/design document in 3 phases. Goal: eliminate at write-time the gaps that review catches.

### Phase 1: Requirements Gathering

Determine spec type from argument or infer from conversation. Only ask if unclear.

| Type | Use Case | Template |
|------|----------|----------|
| `feature` | Feature spec (UI/screens/flows) | references/feature-template.md |
| `api` | REST/GraphQL API endpoint spec | references/api-template.md |
| `system` | System design / architecture | references/system-template.md |
| `data` | Data model / schema spec | references/data-template.md |

Gather **at minimum** (do not re-ask what's already in conversation, code, or CHANGELOG):

**Common required items**
1. Purpose / background
2. Target users / usage scenarios
3. Scope (included / excluded)
4. Related existing features / dependencies

**Type-specific additional items**
- `feature`: Main flow, screen transitions, inputs/outputs, states
- `api`: Endpoints, request/response, authentication, error responses
- `system`: Component architecture, data flow, external system integration
- `data`: Entities, attributes, relationships, constraints

Ask everything in one batch. If user says "up to you", make reasonable assumptions and document them as `Assumption: ...`.

### Phase 2: Draft Generation

Cover all aspects (aligned with review Round 2 checklist):

**A. Requirements Completeness** — user stories, CRUD explicitly, inputs/outputs/state transitions

**B. Eliminate Contradictions and Ambiguity** — no "appropriately"/"as much as possible"; use numbers; consistent terminology + glossary

**C. Non-Functional Requirements** — performance, security, availability, monitoring, scalability (mark N/A with reason; omission not allowed)

**D. Edge Cases / Error States** — boundary values, concurrency, network failure, invalid input, auth failure

**E. Acceptance Criteria** — Given/When/Then format, testable granularity, happy + error paths

### Phase 3: Self-Review, Spec Items, and Save

Self-review checklist before saving:

```
- [ ] A. Requirements completeness
- [ ] B. Contradictions/ambiguity resolved
- [ ] C. Non-functional requirements documented or N/A
- [ ] D. Edge cases covered
- [ ] E. Acceptance criteria in GWT format
```

After self-review passes:

1. Bootstrap directories if needed:
   ```bash
   mkdir -p specs/todo specs/inprogress specs/done
   ```

2. Save to `specs/todo/YYYYMMDD-<slug>.md` (date = today, slug from command arg)

3. Include frontmatter:
   ```yaml
   ---
   title: <Spec Title>
   type: feature | api | system | data
   status: todo
   author: <from git config user.name or "unknown">
   created: <YYYY-MM-DD>
   reviewed: false
   related: []
   ---
   ```

4. Append **Spec Items** section at the bottom:

   ```markdown
   ## Spec Items

   | ID | Requirement | Priority |
   |----|-------------|----------|
   | SPEC-001 | User can create a payment with a positive amount | P0 |
   | SPEC-002 | System rejects payments with amount ≤ 0 | P0 |
   | SPEC-003 | Payment confirmation email sent within 5s | P1 |
   ```

   Priority: `P0` = must merge, `P1` = feature complete, `P2` = deferrable.

   Number sequentially from `SPEC-001`, or continue from last ID if other specs exist in the project.

5. Present save path + 3-line summary. Suggest: `/spec review <spec-id>` next.

**Notes:**
- Read existing `README.md`, `CHANGELOG.md`, and other specs first
- Specs document WHAT, not HOW — minimal code examples
- Match user's conversation language
- On update: set `status: revised`, append change history

---

## `/spec review <spec-id>`

Structurally review a spec in 3 rounds. **Do not write code during review.**

### Step 0: Load spec

```bash
SPEC_FILE=$(find specs/todo specs/inprogress specs/done -name "*${SPEC_ID}*.md" 2>/dev/null | head -1)
```

Read the file with Read tool. If not found, list available specs and stop.

### Round 1: Overall Understanding

Grasp:
- Purpose, scope, target users
- Feature list and main flows
- Prerequisites and constraints
- Document structure

Summarize in 1–3 sentences before Round 2.

### Round 2: Parallel Perspective Check

Analyze all 4 perspectives simultaneously:

**A. Requirements Completeness**
- Missing functional requirements (CRUD each defined?)
- User stories / use cases coverage
- Inputs, outputs, state transitions defined?

**B. Contradictions & Ambiguity**
- Cross-section contradictions
- Vague phrases ("appropriately", "as much as possible")
- Inconsistent terminology for same concept

**C. Non-Functional Requirements**
- Performance (response time, throughput)
- Security (auth, authorization, data protection)
- Availability, failure handling, monitoring
- Scalability

**D. Edge Cases**
- Boundary values, extreme inputs
- Concurrent access / race conditions
- Error handling and failure flows
- Missing data / null / empty

Also verify the **Spec Items** table: every testable requirement has a `SPEC-NNN` ID; vague items flagged.

### Round 3: Prioritized Output

```
## Review Results — <spec-id>

### 🔴 Critical (must fix before build)
- [perspective] Issue → recommended fix

### 🟡 Major (fix recommended)
- [perspective] Issue → recommended fix

### 🟢 Minor (improvement)
- [perspective] Issue → recommended fix

### Spec Items Check
- Missing IDs: <list or "none">
- Untestable items: <list or "none">

### Summary
Overall quality assessment in 2–3 sentences.
```

**Priority criteria:**
- Critical: unimplementable, major security risk, missing business requirement
- Major: ambiguity causing rework, missing important NFR
- Minor: readability, maintainability, future extensibility

### After review

If Critical/Major findings exist: update the spec to address them, then re-run review or confirm fixes with user.

When review passes (no open Critical):
1. Update spec frontmatter: `reviewed: true`, `review_date: YYYY-MM-DD`
2. Keep file in `specs/todo/` until build starts
3. Suggest: `/spec build <spec-id>`

---

## `/spec build <spec-id>`

Implement from a reviewed spec. Requires spec to be reviewed (no open 🔴 Critical).

### Step 0: Pre-flight

```bash
SPEC_FILE=$(find specs/todo specs/inprogress specs/done -name "*${SPEC_ID}*.md" 2>/dev/null | head -1)
```

Verify:
- [ ] Spec file exists
- [ ] `reviewed: true` in frontmatter (or user explicitly waives review — document waiver)
- [ ] Spec Items table present with P0/P1 items

Move to inprogress if in todo:

```bash
git mv specs/todo/YYYYMMDD-<slug>.md specs/inprogress/
# Update frontmatter: status: inprogress
git commit -m "spec: move <slug> to inprogress"
```

### Step 1: Plan Derivation

Derive implementation plan from Spec Items table. Group by component/layer:

```
Implementation Plan — <spec-id>
===============================
Group 1: Data model [SPEC-001, SPEC-002]
  - Create src/models/payment.ts
  - Add migration: YYYYMMDD_add_payments_table.sql
  Complexity: S

Group 2: Validation [SPEC-002, SPEC-004]
  - Create src/validators/payment.ts
  Complexity: S
```

**Rules:**
- Every task maps to at least one SPEC ID
- Do not add tasks without a SPEC ID — add the spec item first or mark out-of-scope
- Present plan to user before coding (unless user said "just build it")

### Step 2: TDD Implementation

Follow `/tdd-workflow` for each group. SDD constraint: **every test name includes its SPEC ID:**

```typescript
// Good
it("SPEC-002: rejects payment when amount is zero", () => { ... })
it("SPEC-002: rejects payment when amount is negative", () => { ... })

// Bad — no traceability
it("validates payment amount", () => { ... })
```

If writing a test for behavior not in any SPEC ID: stop — add spec item first or confirm it's an implementation detail.

Commit messages reference SPEC IDs: `feat: add payment validation [SPEC-042, SPEC-043]`

### Step 3: Spec Compliance Verification

After P0/P1 implementation:

```bash
SPEC_FILE="specs/inprogress/YYYYMMDD-<slug>.md"

# SPEC IDs in spec
grep -oE 'SPEC-[0-9]+' "$SPEC_FILE" | sort -u > /tmp/spec-ids.txt

# SPEC IDs in tests
grep -rE 'SPEC-[0-9]+' src/ tests/ 2>/dev/null | grep -oE 'SPEC-[0-9]+' | sort -u > /tmp/test-ids.txt

# Unimplemented (must be empty for P0 before merge)
comm -23 /tmp/spec-ids.txt /tmp/test-ids.txt
```

P0 unimplemented IDs must be empty before merge. P1 deferrals need written justification in spec.

If `/verification-loop` is available, run semantic compliance pass in addition to grep.

### Step 4: Close spec

After merge:
```bash
git mv specs/inprogress/YYYYMMDD-<slug>.md specs/done/
# Update frontmatter: status: done
git commit -m "spec: move <slug> to done"
```

---

## Spec Document Conventions

### File naming

```
YYYYMMDD-<feature-slug>.md
```

Examples: `20260617-payment-creation.md`, `20260618-payments-api.md`

- Date = spec creation day (not implementation date)
- Slug = lowercase, hyphens, no spaces, no version numbers

### Directory layout

```
project-root/
  specs/
    todo/          # Written, not yet implementing
    inprogress/    # Actively implementing
    done/          # Merged and verified
```

Never create subdirectories other than `todo/`, `inprogress/`, `done/`. Never put specs inside `src/` or `docs/`.

### Lifecycle transitions

Move files (not copy). Always standalone commit:
```
git commit -m "spec: move <slug> to inprogress"
```

Update `status:` in frontmatter to match directory.

### Handling spec changes during build

1. Update spec first — change document, update/add SPEC IDs
2. Update affected tests
3. Then update implementation
4. Never update code first — inverts the dependency

Verbal/ticket requests: "I'll update the spec first."

---

## Common Pitfalls

1. **Skipping review before build.** Review catches ambiguities 10× cheaper than post-coding discovery. `/spec build` requires reviewed spec.

2. **Retrofitting SPEC IDs after tests.** IDs must exist in spec before writing tests.

3. **Vague spec language.** "Handle errors gracefully" is not a spec item until it says: `SPEC-007: API returns HTTP 422 with {error: string} when validation fails`.

4. **Implementing beyond the spec.** Add to spec or don't build it.

5. **Letting spec drift from code.** Update spec whenever behavior changes.

6. **One giant spec.** Split per-feature/domain. Reference others: `See: 20260618-payments-api`.

7. **Confusing spec items with tasks.** `SPEC-001: user can create payment` is a requirement. "Create Payment model" is a task for the implementation plan.

8. **Path inconsistency.** Always use `specs/todo|inprogress|done/`, not legacy `spec/` directory.

---

## Verification Checklist

### After `/spec create`
- [ ] File at `specs/todo/YYYYMMDD-<slug>.md`
- [ ] Frontmatter complete with `status: todo`, `reviewed: false`
- [ ] Spec Items table with all testable requirements as SPEC-NNN
- [ ] Self-review checklist passed

### After `/spec review`
- [ ] Review output with Critical/Major/Minor sections
- [ ] No open 🔴 Critical findings
- [ ] `reviewed: true` and `review_date` set in frontmatter

### After `/spec build`
- [ ] Spec in `specs/inprogress/` during work, `specs/done/` after merge
- [ ] Implementation plan maps every task to SPEC IDs
- [ ] All tests include SPEC-NNN in name
- [ ] Compliance grep: no unimplemented P0 IDs
- [ ] P1 deferrals documented if any

---

## Template Reference

Detailed structures in `references/`:
- [feature-template.md](references/feature-template.md)
- [api-template.md](references/api-template.md)
- [system-template.md](references/system-template.md)
- [data-template.md](references/data-template.md)
