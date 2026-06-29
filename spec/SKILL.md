---
name: spec
description: "Use when creating, reviewing, or implementing from specification documents. Unified spec-driven workflow via /spec create, /spec review {spec-id}, and /spec build {spec-id}. Treats the spec as single source of truth with SPEC-NNN traceability through TDD implementation."
version: 2.3.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spec, sdd, tdd, requirements, review, build]
    related_skills: [tdd-workflow, verification-loop, blueprint, code-review, council]
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
find specs -maxdepth 1 -name "*${SPEC_ID}*.md" 2>/dev/null | head -1
```

If zero matches: report "spec not found" and list available specs.
If multiple matches: ask user to disambiguate with full date prefix.

### List available specs

```bash
find specs -maxdepth 1 -name '*.md' 2>/dev/null \
  | sort \
  | while read f; do
      basename "$f" .md
      grep -m1 '^status:' "$f" 2>/dev/null || echo "  (no status field)"
    done
```

---

## `/spec create <slug> [type]`

Create a specification/design document in **5 phases**. Goal: right-sized specs that are feasible before draft is saved.

**Hard gates — do not skip:**
1. Phase 1.6 must resolve all blockers before Phase 2.
2. Phase 2 includes **only** sections selected in Phase 1.5 — never dump the full template.

### Phase 1: Requirements Gathering

Determine spec type from argument or infer from conversation. Only ask if unclear.

| Type | Use Case | Template (reference only) |
|------|----------|---------------------------|
| `feature` | Feature spec (UI/screens/flows) | references/feature-template.md |
| `api` | REST/GraphQL API endpoint spec | references/api-template.md |
| `system` | System design / architecture | references/system-template.md |
| `data` | Data model / schema spec | references/data-template.md |

Templates are **full catalogs**, not mandatory output. Section selection is in Phase 1.5 via [section-catalog.md](references/section-catalog.md).

Gather **at minimum** (do not re-ask what's already in conversation, code, or CHANGELOG):

**Common required items**
1. Purpose / background
2. Target users / usage scenarios (skip if obviously single-role internal tool)
3. Scope (included / excluded)
4. Related existing features / dependencies

**Type-specific additional items**
- `feature`: Main flow, screen transitions, inputs/outputs, states (only if applicable)
- `api`: Endpoints, request/response, authentication, error responses
- `system`: Component architecture, data flow, external system integration
- `data`: Entities, attributes, relationships, constraints

Ask only **missing** items in one batch. If user says "up to you", make reasonable assumptions and document them as `Assumption: ...` — but still run Phase 1.6 for external/platform constraints.

### Phase 1.5: Sizing & Section Selection

Before drafting, classify complexity and pick sections. Read [section-catalog.md](references/section-catalog.md).

| Tier | Typical scope | Spec size target |
|------|---------------|------------------|
| `minimal` | Single behavior, one endpoint, config toggle, ≤3 SPEC items | ~50–120 lines |
| `standard` | Multi-step flow, several endpoints, 4–15 SPEC items | ~120–250 lines |
| `full` | New subsystem, cross-cutting, compliance-critical, 15+ SPEC items | 250+ lines |

**Workflow:**
1. Infer tier from scope and SPEC item count estimate.
2. Build a **Section Plan** table: section name → include / exclude + one-line reason.
3. If tier is ambiguous, present plan to user: "This looks `minimal` — skip NFR and UI table. OK?"
4. Record in spec frontmatter: `complexity: minimal | standard | full`

**Rules:**
- ✅ Always: Overview, functional requirements, acceptance criteria, Spec Items.
- ⚠️ Conditional: include only when catalog criteria match (e.g., state transitions only for stateful entities).
- ⬜ Omit: do **not** fill with "N/A" boilerplate — list in `## Excluded Sections` instead.
- Never pad a `minimal` spec to look like `full`.

### Phase 1.6: Feasibility & Clarification Gate

**Stop and ask the user** before Phase 2 when any requirement depends on external/platform capability, unknown constraints, or conflicting goals.

#### 1.6.1 Investigate before assuming

For each requirement touching external systems, APIs, SDKs, or platform features:

1. Read project code, config, README, existing specs.
2. Check official docs (Context7, vendor docs, or web search) — not training-data memory alone.
3. Classify each item:

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Verified | Documented capability or already in codebase | Proceed |
| ⚠️ Unverified | Docs unclear, version-dependent, or needs product decision | Ask user |
| ❌ Blocked | Officially unsupported, impossible, or contradicts stated platform limits | Ask user; do not spec as-is |

**Examples of ❌ Blocked:**
- "Expose Cursor ACP max mode toggle" when official ACP API does not expose max mode → blocked until user picks an alternative (e.g., document manual UI step, file upstream feature request, or drop requirement).
- "Real-time sync <50ms" on serverless cold-start with no infra budget → blocked until scope or infra is clarified.

#### 1.6.2 Present Clarification Checklist

Output this **before** drafting. Wait for user response on every ⚠️ and ❌ row.

```markdown
## Clarification Checklist — <slug>

| # | Requirement | Status | Finding | Question / Alternatives |
|---|-------------|--------|---------|-------------------------|
| 1 | Max mode via Cursor ACP | ❌ Blocked | Not in official ACP API (checked: <source>) | Drop / workaround / out-of-scope? |
| 2 | Target p95 latency | ⚠️ Unverified | No baseline in codebase | What p95 is acceptable? |

**Cannot save draft until:** all ❌ resolved (drop, workaround, or explicit waive) and all ⚠️ answered or waived.
```

For ❌ items, always offer 2–3 concrete alternatives (drop, defer, workaround, scope change) — never silently rewrite the requirement.

#### 1.6.3 Gate rules

- **Do not** enter Phase 2 while any ❌ remains open.
- **Do not** write requirements the user has not confirmed after a ❌/⚠️ finding.
- User waiver: record in spec as `Assumption (user-waived): ...` or move to Out of scope.
- If user says "spec it anyway" for a ❌ item: move requirement to **Out of scope** or **Future / blocked dependency** — never P0 Spec Items.

### Phase 2: Draft Generation

Generate **only sections from Phase 1.5 Section Plan**. Apply quality rules to included sections:

**A. Requirements Completeness** (included sections) — user stories if selected; CRUD only for affected resources; inputs/outputs/state transitions where relevant

**B. Eliminate Contradictions and Ambiguity** — no "appropriately"/"as much as possible"; use numbers; glossary only if selected

**C. Non-Functional Requirements** — only selected NFR subsections; each documents target or `N/A — <reason>` inside that subsection

**D. Edge Cases / Error States** — cover edges that change behavior; skip irrelevant categories (e.g., skip concurrency for read-only config)

**E. Acceptance Criteria** — Given/When/Then, testable, happy + error paths for in-scope behavior

Add `## Excluded Sections` when any template section was omitted (see section-catalog).

### Phase 3: Self-Review, Spec Items, and Save

Self-review checklist before saving:

```
- [ ] Phase 1.6: no open ❌ blockers; ⚠️ items answered or waived
- [ ] Phase 1.5: only planned sections present; Excluded Sections documented
- [ ] A. Requirements completeness (for included sections)
- [ ] B. Contradictions/ambiguity resolved
- [ ] C. NFR subsections included or omitted per plan (not blank placeholders)
- [ ] D. Relevant edge cases covered
- [ ] E. Acceptance criteria in GWT format
- [ ] No P0 Spec Items for blocked/unverified platform capabilities
```

After self-review passes:

1. Bootstrap directory if needed:
   ```bash
   mkdir -p specs
   ```

2. Save to `specs/YYYYMMDD-<slug>.md` (date = today, slug from command arg)

3. Include frontmatter:
   ```yaml
   ---
   title: <Spec Title>
   type: feature | api | system | data
   complexity: minimal | standard | full
   status: draft
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
- **Right-size over completeness:** a 80-line `minimal` spec beats a 400-line spec with empty N/A sections
- **Feasibility over optimism:** if official docs don't support a capability, surface it in Phase 1.6 — don't bury in Risks after save

---

## `/spec review <spec-id>`

Structurally review a spec in 3 rounds via **isolated subagent(s)**. The parent agent orchestrates; it does **not** perform the review inline. **Do not write code during review.**

### Step 0: Resolve and validate (parent)

```bash
SPEC_FILE=$(find specs -maxdepth 1 -name "*${SPEC_ID}*.md" 2>/dev/null | head -1)
```

If not found: list available specs and stop.

Read the spec once to confirm it loads. Do not start Round 1 analysis in the parent — delegate all review work to subagent(s).

### Step 1: Launch review subagent(s)

Use the **Task** tool. Default: **one `generalPurpose` subagent** with `readonly: true` running the full 3-round review.

For large specs (>300 lines) or high-stakes features, fan out **4 parallel subagents** (one per perspective A/B/C/D below) and synthesize Round 3 in the parent. Do not run inline review as a fallback unless subagent launch fails twice.

**Task invocation (single reviewer — default):**

```text
Task(
  description: "Spec review <spec-id>",
  subagent_type: "generalPurpose",
  readonly: true,
  prompt: "<REVIEWER_PROMPT below>"
)
```

**Task invocation (parallel — large/high-stakes only):**

Launch 4 Tasks concurrently, each with the same prompt but a different `Perspective:` line (A, B, C, or D). Parent synthesizes Round 3 from all four outputs.

#### REVIEWER_PROMPT

Pass this exact shape to the subagent. Replace placeholders; do not include parent conversation history.

```text
You are an independent spec reviewer. You have no implementation context and no stake in approving the spec. Your job is to find problems.

Spec file (read with Read tool):
  <absolute path to SPEC_FILE>

Spec ID: <spec-id>

## Your workflow

### Round 1: Overall Understanding
Read the spec. Grasp purpose, scope, target users, feature list, main flows, prerequisites, constraints, and document structure.
Output a 1–3 sentence summary.

### Round 2: Perspective Check
Analyze from this lens (parallel mode: only your assigned perspective; single mode: all four):

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

**E. Feasibility & Platform Constraints**
- Requirements depending on external API/platform features — are they documented/supported?
- P0 items that are technically impossible or unverified
- Blocked items incorrectly left in scope vs moved to Out of scope / Future

Also verify the Spec Items table: every testable requirement has a SPEC-NNN ID; flag vague or untestable items.

Perspective (parallel mode only): <A|B|C|D>

### Round 3: Prioritized Output

Return exactly this structure:

## Review Results — <spec-id>

### Round 1 Summary
<1–3 sentences>

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

## Priority criteria
- Critical: unimplementable, unsupported platform/API capability in P0, major security risk, missing business requirement
- Major: ambiguity causing rework, missing important NFR, unverified assumptions not flagged
- Minor: readability, maintainability, future extensibility, over-sized spec with unnecessary sections

Be rigorous. Cite section names and exact phrases. Do not approve vague specs to be polite.
```

### Step 2: Handle subagent failures (parent)

- If Task fails due to bad invocation (missing path, wrong type): fix and retry once immediately.
- If subagent returns empty or malformed output: retry once with the same prompt.
- If failure persists after retry: report the blocker to the user. Do not fall back to inline review unless user explicitly asks.

### Step 3: Synthesize and present (parent)

**Single subagent:** Present the subagent output as-is (minor formatting cleanup only).

**Parallel subagents:** Merge findings into one Round 3 block. Deduplicate identical issues. Preserve all Critical/Major findings from any perspective.

Present to user. Do not edit the spec during review — only report findings.

### Step 4: After review (parent)

If Critical/Major findings exist: offer to update the spec to address them, then re-run `/spec review <spec-id>` (spawns fresh subagent(s)).

When review passes (no open 🔴 Critical):
1. Update spec frontmatter: `reviewed: true`, `review_date: YYYY-MM-DD`, `status: reviewed`
2. Suggest: `/spec build <spec-id>`

---

## `/spec build <spec-id>`

Implement from a reviewed spec. Requires spec to be reviewed (no open 🔴 Critical).

### Step 0: Pre-flight

```bash
SPEC_FILE=$(find specs -maxdepth 1 -name "*${SPEC_ID}*.md" 2>/dev/null | head -1)
```

Verify:
- [ ] Spec file exists
- [ ] `reviewed: true` in frontmatter (or user explicitly waives review — document waiver)
- [ ] Spec Items table present with P0/P1 items

Update frontmatter to mark build start:

```yaml
status: inprogress
```

Commit the status change with implementation work or as a standalone commit:
```
git commit -m "spec: start build for <slug>"
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
SPEC_FILE="specs/YYYYMMDD-<slug>.md"

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

After merge, update frontmatter in place:

```yaml
status: done
```

Commit with implementation merge or standalone:
```
git commit -m "spec: mark <slug> done"
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
    20260617-payment-creation.md
    20260618-payments-api.md
```

All specs live flat under `specs/`. Never put specs inside `src/` or `docs/`. Do not create subdirectories under `specs/`.

### Lifecycle (frontmatter only)

Track state via `status:` in frontmatter — no file moves:

| status | Meaning |
|--------|---------|
| `draft` | Just created, not yet reviewed |
| `reviewed` | Review passed, ready to build |
| `inprogress` | Actively implementing |
| `done` | Implemented and verified |
| `revised` | Updated after initial review/build |

Update `status:` when phase changes. Commit status updates with related work or standalone.

### Handling spec changes during build

1. Update spec first — change document, update/add SPEC IDs
2. Update affected tests
3. Then update implementation
4. Never update code first — inverts the dependency

Verbal/ticket requests: "I'll update the spec first."

---

## Common Pitfalls

1. **Inline review in parent.** `/spec review` must spawn subagent(s). Parent only resolves path, launches Task, synthesizes, updates frontmatter.

2. **Skipping review before build.** Review catches ambiguities 10× cheaper than post-coding discovery. `/spec build` requires reviewed spec.

3. **Passing conversation history to reviewer.** Subagent gets spec path + REVIEWER_PROMPT only. No parent chat log — prevents implementation bias.

4. **Retrofitting SPEC IDs after tests.** IDs must exist in spec before writing tests.

5. **Vague spec language.** "Handle errors gracefully" is not a spec item until it says: `SPEC-007: API returns HTTP 422 with {error: string} when validation fails`.

6. **Implementing beyond the spec.** Add to spec or don't build it.

7. **Letting spec drift from code.** Update spec whenever behavior changes.

8. **One giant spec.** Split per-feature/domain. Reference others: `See: 20260618-payments-api`.

9. **Confusing spec items with tasks.** `SPEC-001: user can create payment` is a requirement. "Create Payment model" is a task for the implementation plan.

10. **Path inconsistency.** Always use flat `specs/YYYYMMDD-<slug>.md`. No subdirectories, no legacy `spec/` directory.

11. **Fixed-size specs.** Dumping every template section regardless of scope bloats docs and hides signal. Use Phase 1.5 + section-catalog.

12. **Specifying the impossible.** Writing P0 items for capabilities absent from official APIs (e.g., unsupported ACP options) wastes review/build cycles. Phase 1.6 gate first.

13. **Silent assumption on platform limits.** "Should work" is not verification. Check docs/code; ask user when ❌/⚠️.

## Verification Checklist

### After `/spec create`
- [ ] Phase 1.5 Section Plan applied; `complexity` in frontmatter
- [ ] Phase 1.6 Clarification Checklist resolved (no open ❌)
- [ ] File at `specs/YYYYMMDD-<slug>.md`
- [ ] Frontmatter complete with `status: draft`, `reviewed: false`
- [ ] Spec Items table with all testable requirements as SPEC-NNN
- [ ] No P0 items for blocked platform capabilities
- [ ] Self-review checklist passed

### After `/spec review`
- [ ] Review delegated to subagent(s) via Task tool (`readonly: true`)
- [ ] Review output with Critical/Major/Minor sections
- [ ] No open 🔴 Critical findings
- [ ] `reviewed: true` and `review_date` set in frontmatter

### After `/spec build`
- [ ] Frontmatter `status: inprogress` during work, `status: done` after merge
- [ ] Implementation plan maps every task to SPEC IDs
- [ ] All tests include SPEC-NNN in name
- [ ] Compliance grep: no unimplemented P0 IDs
- [ ] P1 deferrals documented if any

---

## Template Reference

Full template structures (pick sections via catalog — do not copy wholesale):
- [section-catalog.md](references/section-catalog.md) — **start here for sizing**
- [feature-template.md](references/feature-template.md)
- [api-template.md](references/api-template.md)
- [system-template.md](references/system-template.md)
- [data-template.md](references/data-template.md)
