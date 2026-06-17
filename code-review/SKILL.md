---
name: code-review
description: "Use when reviewing a PR/MR/diff, auditing a change for correctness/security/performance, or when asked 'review this', 'is this safe to merge', or '/code-review'. Synthesizes Google eng-practices (Standard of Code Review + 12 dimensions), the OWASP secure-code-review lens, and modern AI-reviewer prompt patterns into one operational workflow. Pairs with the dev_workspace skill for clone-first sandbox mechanics."
version: "1.0.0"
author: Kizuki Aiki
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, security, owasp, google-eng-practices, pr-review]
    related_skills: [dev_workspace]
  last_updated: "2026-06-17"
  sources:
    - "Google eng-practices: The Standard of Code Review"
    - "Google eng-practices: What to look for in a code review"
    - "OWASP Code Review Guide v2"
---

# Code Review

## Overview

A code review's job is **not** to prove you're smart or to make the code perfect. It is to make sure **the overall code health of the codebase improves over time** while shipping the change. This skill turns that principle into a repeatable, sandbox-aware workflow with a concrete checklist, a security lens, and an output contract.

> **The one rule that resolves most disputes:** Approve when the change **definitely improves overall code health**, even if it isn't perfect. Aim for *continuous improvement*, not perfection. Never block a net-positive CL just because you can imagine a more ideal version that doesn't exist yet. — *Google, The Standard of Code Review*

## Core Philosophy

| Principle | What it means in practice |
|---|---|
| **Code health > perfection** | Ask "is the codebase healthier *after* this merges?" not "is this what I would have written?" |
| **Continuous improvement** | A CL that improves things but leaves room for more is still a YES. File a follow-up, don't gate the merge. |
| **Facts & data over opinion** | Technical facts outweigh preference. "This is slower because of the O(n²) loop" wins; "I don't like this style" does not. |
| **Mentor, don't gatekeep** | Leave educational comments. Mark optional ones so the author knows what's actually required. |
| **Praise out loud** | If something is done well — especially if the author addressed earlier feedback — say so. Reviews are not only for finding faults. |
| **Never leave a CL stuck** | If you disagree, drive to resolution: discuss → sync call (record the outcome in the thread) → escalate. Don't ghost a PR. |

## When To Use

- Reviewing a GitHub PR / GitLab MR / raw diff (`review this PR`, `/code-review`, `is this mergeable?`).
- Pre-merge correctness / security / performance audit of a change.
- "Second opinion" pass on your own change before requesting human review.

## When NOT To Use (or scale down)

- Pure metadata questions ("who authored this?", "how many open PRs?") → just `gh pr view`, no review machinery.
- Generated/lock/vendored files → scan, don't line-review (see *Every Line* exception).
- The user wants a quick gut-check, not an audit → give the verdict + top 3 risks only.

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

## Review Workflow (sandbox-aware)

> Clone mechanics, `gh` auth/identity caveats, parallel rounds, and the fine-grained-PAT Checks-API workaround live in the **`dev_workspace`** skill. Load it first for any GitHub PR. This skill assumes the diff is already in front of you.

**Pre-flight:** run `gh auth status`. If not logged in, STOP — report no GitHub auth, don't speculate file paths. (See `dev_workspace`.)

```
Round 1 (parallel): clone + checkout PR  ||  gh pr view --json title,body,labels,additions,deletions,changedFiles -R owner/repo  ||  gh pr diff -R owner/repo
Round 2 (parallel): read every changed file locally with `view`; grep_file for the security patterns
Round 3: (optional, deep/max-effort) fan out delegate_work lenses — correctness, security, first-principles
Round 4: synthesize → single output, no duplication
```

Method, in order:
1. **Read the PR description first.** Understand intent before judging code. A diff that's correct but solves the wrong problem is still wrong.
2. **Read in broad context, not just changed lines.** Open the whole file when needed — a locally-fine change can be globally wrong (see *Context* in the checklist).
3. **Walk the checklist** — `references/review_checklist.md` (the 12 Google dimensions + concurrency + performance).
4. **Run the security lens** — `references/security_review.md` (OWASP-flavored; concrete grep targets).
5. **For hard calls, use the prompt patterns** — `references/reviewer_prompts.md` ("top 3 risks", "what breaks at 10×", first-principles, root-cause).
6. **Verify, don't assume.** If tests exist and the repo is cloned, run them (`make test` / `pytest` / `npm test`). CI-green supplements local verify; it doesn't replace reading the tests.
7. **Write the verdict** in the output format below.

## Output Format

```markdown
## Summary
What the PR does and why, in 2–3 sentences. (Proves you understood it.)

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

Verdict guidance: **LGTM** the moment the change improves code health and has no 🔴. Outstanding 🟡/🟢 can ride a follow-up; don't withhold approval to chase perfection.

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

## Verification Checklist

- [ ] PR description read before judging any code
- [ ] All changed files opened in full context (not diff-only)
- [ ] All 12 review dimensions walked (`references/review_checklist.md`)
- [ ] Security lens applied (`references/security_review.md`)
- [ ] Every finding tagged with 🔴/🟡/🟢/💙
- [ ] At least one 💙 Praise on any non-trivial PR
- [ ] Output matches the required format (Summary / Findings / Verdict)
- [ ] No merge blocked solely on Nit-level items

## Reference Files

| File | Use it for |
|---|---|
| `references/review_checklist.md` | The full multi-dimension checklist (Design → Good Things) + concurrency + performance, as actionable questions. |
| `references/security_review.md` | OWASP-flavored security audit lens with concrete grep targets. |
| `references/reviewer_prompts.md` | AI-reviewer prompt patterns + how to write constructive, citable comments. |
