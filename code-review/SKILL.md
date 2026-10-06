---
name: code-review
description: "Use when reviewing a PR/MR/diff, auditing a change for correctness/security/performance, or when asked 'review this', 'is this safe to merge', or '/code-review'. Always launches Task subagents for independent review. Synthesizes Google eng-practices (Standard of Code Review + 12 dimensions), the OWASP secure-code-review lens, adversarial verification (falsify claims before approving), and modern AI-reviewer prompt patterns. Pairs with the dev_workspace skill for clone-first sandbox mechanics."
disable-model-invocation: true
version: "1.2.0"
author: Kizuki Aiki
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, security, owasp, google-eng-practices, pr-review, adversarial-verification, subagent]
    related_skills: [dev_workspace]
  last_updated: "2026-07-23"
  sources:
    - "Google eng-practices: The Standard of Code Review"
    - "Google eng-practices: What to look for in a code review"
    - "OWASP Code Review Guide v2"
    - "Adversarial verification: falsify author claims before approval"
---

# Code Review

## Overview

A code review's job is **not** to prove you're smart or to make the code perfect. It is to make sure **the overall code health of the codebase improves over time** while shipping the change. This skill turns that principle into a repeatable, sandbox-aware workflow with a concrete checklist, a security lens, **adversarial verification**, **mandatory subagent review**, and an output contract.

> **The one rule that resolves most disputes:** Approve when the change **definitely improves overall code health**, even if it isn't perfect. Aim for *continuous improvement*, not perfection. Never block a net-positive CL just because you can imagine a more ideal version that doesn't exist yet. — *Google, The Standard of Code Review*

> **Adversarial verification:** Quality is checked by an independent reviewer who assumes the work **may be wrong** and deliberately tries to **falsify** its claims. Approval means the claims survived attack — not that the author's story sounded good.

> **Subagents required:** The parent agent briefs and synthesizes; **review work runs in `Task` subagents** so the attacker is not the same context that wrote or championed the change. See `references/subagent-orchestration.md`.

## Core Philosophy

| Principle | What it means in practice |
|---|---|
| **Code health > perfection** | Ask "is the codebase healthier *after* this merges?" not "is this what I would have written?" |
| **Continuous improvement** | A CL that improves things but leaves room for more is still a YES. File a follow-up, don't gate the merge. |
| **Facts & data over opinion** | Technical facts outweigh preference. "This is slower because of the O(n²) loop" wins; "I don't like this style" does not. |
| **Falsify, then approve** | Start from "what would prove this wrong?" Extract claims → invert → hunt counterexamples → attack the tests-as-proof. Surviving that pass is the bar. |
| **Independent reviewer via subagent** | Launch `Task` subagent(s) for the review. Parent does not solitary-review. Own-change second opinions must use a subagent as the primary attacker. |
| **Mentor, don't gatekeep** | Leave educational comments. Mark optional ones so the author knows what's actually required. |
| **Praise out loud** | If something is done well — especially if the author addressed earlier feedback — say so. Reviews are not only for finding faults. |
| **Never leave a CL stuck** | If you disagree, drive to resolution: discuss → sync call (record the outcome in the thread) → escalate. Don't ghost a PR. |

## When To Use

- Reviewing a GitHub PR / GitLab MR / raw diff (`review this PR`, `/code-review`, `is this mergeable?`).
- Pre-merge correctness / security / performance audit of a change.
- "Second opinion" pass on your own change before requesting human review (switch roles: attack only what the diff guarantees).

## When NOT To Use (or scale down)

- Pure metadata questions ("who authored this?", "how many open PRs?") → just `gh pr view`, no review machinery (no subagent).
- Generated/lock/vendored files → scan, don't line-review (see *Every Line* exception).
- The user wants a quick gut-check, not an audit → still launch **one** adversarial subagent; return verdict + top 3 risks (lite claim inversion). Parent must not skip the subagent.

## Severity Taxonomy (label EVERY finding)

Tag each comment so the author instantly knows the bar. This is the highest-leverage habit in the whole skill.

| Tag | Meaning | Blocks merge? |
|---|---|---|
| 🔴 **Blocking** | Correctness bug, security hole, data loss, breaking change, missing critical test. | **Yes** |
| 🟡 **Should-fix** | Real design/maintainability/perf concern that should be addressed now or in a tracked follow-up. | Author's call + judgment |
| 🟢 **Nit** | Style, naming polish, micro-optimization, personal preference. Purely optional. | **No** |
| 💙 **Praise** | Something done well. Reinforce it. | n/a |

Rules:
- Prefix optional/educational comments with **`Nit:`** so they never read as a merge gate.
- Do **not** require perfection on `Nit`-level items. Personal preference alone is never blocking.
- If you only produce 🔴/🟡 and zero 💙 across a non-trivial PR, you're reviewing wrong.
- A falsified load-bearing claim with a concrete counterexample is usually 🔴 or 🟡 — never bury it as a Nit.

## Review Workflow (sandbox-aware)

> Clone mechanics, `gh` auth/identity caveats, parallel rounds, and the fine-grained-PAT Checks-API workaround live in the **`dev_workspace`** skill. Load it first for any GitHub PR. This skill assumes the diff is already in front of you.

**Pre-flight:** run `gh auth status`. If not logged in, STOP — report no GitHub auth, don't speculate file paths. (See `dev_workspace`.)

```
Round 1 (parent, parallel): clone + checkout PR  ||  gh pr view --json ...  ||  gh pr diff
Round 2 (parent): brief only — PR intent, file list, how to obtain the diff. Do NOT solitary-review.
Round 3 (required, parallel Task subagents): launch per references/subagent-orchestration.md
         — always: adversarial-correctness (generalPurpose)
         — when applicable: security lens (generalPurpose)
         — optional deep: first-principles / edge-cases
Round 4 (subagents): checklist + security + adversarial falsification inside each lens
Round 5 (parent): synthesize subagent outputs → single Output Format, no duplication
```

Method, in order:
1. **Parent: read the PR description / metadata first** enough to brief subagents. Understand stated intent.
2. **Parent: launch `Task` subagent(s) immediately** — required. Follow `references/subagent-orchestration.md`. Use `subagent_type: generalPurpose`, `run_in_background: false`. Pass full briefing (repo path, scope, PR body, changed files, diff instructions, lens, skill reference paths).
3. **Subagents: review in context** — full files when needed; walk `references/review-checklist.md`; security lens via `references/security-review.md` when that is their lens.
4. **Subagents: adversarial verification (required)** — `references/adversarial-verification.md`. Assume wrong; falsify claims; attack tests-as-proof. Prompt patterns: `references/reviewer-prompts.md`.
5. **Verify, don't assume.** Subagents (or parent after) run tests if present (`make test` / `pytest` / `npm test`). CI-green does not replace reading or attacking tests.
6. **Parent: synthesize** deduped Findings + merged Adversarial verification + one Verdict. If any subagent reports 🔴, do not LGTM until addressed. If Task failed, report failure and stop — no silent solo review.

## Output Format

```markdown
## Summary
What the PR does and why, in 2–3 sentences. (Proves you understood it.)

## Adversarial verification
Claims attacked: <short list of load-bearing claims>
- Falsified: <counterexample → finding, or "none">
- Survived: <what held up under attack>
- Untested / unverifiable: <ask or 🟡/🔴 if merge-critical>

## Findings
🔴 Blocking
- `path/file.py:42` — <issue>. Why it matters: <impact>. Suggested fix: <action>.

🟡 Should-fix
- `path/file.ts:108` — <concern>. Why: <reason>.

🟢 Nit
- `path/file.go:12` — Nit: <polish>.

💙 Praise
- Clean separation of X / good test coverage on Y.

## Verdict: [✅ LGTM | ✅ LGTM with nits | 🟡 Needs changes | 🛑 Blocked]
<If not LGTM: the specific, ordered, actionable items required to flip to LGTM.>
```

Verdict guidance: **LGTM** only when (1) the change improves code health, (2) there is no 🔴, and (3) adversarial verification found no falsified load-bearing claim left unaddressed. Outstanding 🟡/🟢 can ride a follow-up; don't withhold approval to chase perfection. Do **not** LGTM solely because the author's explanation was persuasive.

## Common Pitfalls

- ❌ **Demanding perfection.** Blocking a net-positive CL over hypothetical ideals. → Approve + file follow-ups.
- ❌ **Only criticizing.** Zero praise on good work kills morale and trust. → Always call out 💙.
- ❌ **Unlabeled severity.** Author can't tell a bug from a preference. → Tag every finding.
- ❌ **Style bikeshedding as a blocker.** → Prefix `Nit:`, never gate on it. Defer to the repo's style guide / linter as the authority.
- ❌ **Reviewing only the diff.** Missing the surrounding file's invariants. → Read in context.
- ❌ **Skipping lines you don't understand.** → Ask the author, or pull in a qualified reviewer (security/concurrency/privacy/i18n). Never rubber-stamp.
- ❌ **"WHAT" without "WHY".** "Change this" with no reasoning teaches nothing and invites pushback. → Always explain the why.
- ❌ **Ghosting a disagreement.** → Drive to resolution or escalate; never leave the PR stuck.
- ❌ **Speculating when a tool fails.** Clone/auth failed → say so and stop. Don't invent file contents from priors.
- ❌ **Confirmation-only review.** Agreeing with the PR story without trying to falsify it. → Run adversarial verification before the verdict.
- ❌ **Adversarial theater.** Inventing speculative "what if someday" issues or style nits dressed as falsification. → Concrete counterexamples only.
- ❌ **Solo review.** Parent producing the full Findings/Verdict without launching a subagent. → Always use `Task` per `subagent-orchestration.md`.
- ❌ **Silent Task fallback.** Subagent failed, so parent "just reviews anyway" and presents it as a full `/code-review`. → Report the failure.

## Verification Checklist

- [ ] PR description / metadata read enough to brief subagents
- [ ] ≥1 `Task` subagent launched (`generalPurpose`); security subagent when scope warrants
- [ ] Subagents opened changed files in full context (not diff-only)
- [ ] Checklist / security / adversarial verification executed inside subagents
- [ ] Parent synthesized (deduped) — did not solitary-author the review
- [ ] Output includes an **Adversarial verification** section
- [ ] Every finding tagged with 🔴/🟡/🟢/💙
- [ ] At least one 💙 Praise on any non-trivial PR
- [ ] Output matches the required format (Summary / Adversarial verification / Findings / Verdict)
- [ ] No merge blocked solely on Nit-level items
- [ ] No LGTM while a falsified load-bearing claim remains open

## Reference Files

| File | Use it for |
|---|---|
| `references/subagent-orchestration.md` | **Required.** When/how to launch `Task` subagents, briefing template, parent synthesis rules. |
| `references/review-checklist.md` | The full multi-dimension checklist (Design → Good Things) + concurrency + performance, as actionable questions. |
| `references/security-review.md` | OWASP-flavored security audit lens with concrete grep targets. |
| `references/adversarial-verification.md` | Required falsification pass: extract claims → invert → counterexamples → attack tests-as-proof. |
| `references/reviewer-prompts.md` | AI-reviewer prompt patterns + how to write constructive, citable comments. |
