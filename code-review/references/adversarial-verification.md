# Adversarial Verification

A mandatory pass: **someone other than the author** tries to **falsify** the change under the premise that **it may be wrong**. Surviving that attempt is the quality signal — not agreeing with the author's story.

> Do not start from "does this look right?" Start from "what would prove this wrong?" Confirmation bias is the failure mode this pass exists to catch.

This is broader than the security **Adversary pass** (malicious input). Here the adversary is epistemic: claims, invariants, tests, and edge cases are on trial.

## Stance

| Do | Don't |
|---|---|
| Assume the PR description, comments, and happy-path tests may be incomplete or wrong | Rubber-stamp because CI is green or the diff "looks clean" |
| Act as an independent reviewer, not a co-author defending the design | Re-derive the author's rationale and stop once it sounds plausible |
| Demand falsifiable claims: "X holds when Y" | Accept vibes: "should be fine", "we handle errors" |
| Prefer concrete counterexamples (input, state, race, rollback) | Vague doubt without a scenario that would break |

When reviewing **your own prior change** (second opinion): do **not** attack it in the same agent context that wrote it. Launch a `Task` subagent as the independent attacker (`subagent-orchestration.md`). The subagent discards author intent and attacks only what the diff + tests actually guarantee.

## Method (run after checklist + security lens, before verdict)

1. **Extract claims.** From the PR description, commit messages, comments, and new tests, list the load-bearing claims (behavior, invariants, non-goals, "we don't support X").
2. **Invert each claim.** For every claim, write the negation or a boundary case that would falsify it.
3. **Hunt counterexamples.** Walk data flow, state transitions, error/retry paths, concurrency, and authz with those negations in mind. Prefer the smallest concrete scenario that breaks the claim.
4. **Attack the proof.** Treat tests as the author's evidence. Ask: would this test still pass if the bug existed? Missing assertion? Testing mocks instead of behavior? No failure-path coverage?
5. **Record outcomes.** Each attack ends as: **falsified** (finding with severity), **survived** (note briefly — this is praise fuel), or **untested / unverifiable** (ask or 🟡 if merge-critical).

## Attack prompts (use as probes)

1. **Claim inversion.** "The PR says it does X. What's the smallest input/state where X is false?"
2. **Hidden premise.** "What must be true for this to work that the diff never states or checks?"
3. **Test as alibi.** "If the claimed bug/regression were still present, which test would fail? If none — the proof is missing."
4. **Complement path.** "Happy path works. What about empty, max, duplicate, stale, concurrent, partial failure, replay?"
5. **Authority swap.** "Ignore the author's explanation. From code alone, what does this actually guarantee? Where do guarantee and story diverge?"
6. **Regression magnet.** "Which nearby invariant did this change quietly invalidate?"
7. **Security adversary (narrow).** Pair with `security-review.md`: untrusted input → sink, missing authz, IDOR.

## What counts as a finding

- A **falsified claim** with a concrete scenario → severity by impact (usually 🔴/🟡).
- An **untested load-bearing claim** that cannot be verified from the diff → 🟡 (or 🔴 if correctness/security-critical) + ask for a test or clarification.
- Claims that **survive** with clear evidence → mention under 💙 or in Summary; do not invent issues to look thorough.

## Anti-patterns for this pass

- ❌ Fishing for style nits and calling it adversarial.
- ❌ Demanding an ideal rewrite when the change is already net-positive and claims hold.
- ❌ Blocking on speculative "what if someday" without a plausible trigger in this codebase.
- ❌ Skipping the pass because the author is trusted or the PR is small — small PRs hide assumption bugs too.
