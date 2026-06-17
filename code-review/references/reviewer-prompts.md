# Reviewer Prompt Patterns & Comment Craft

Two halves: (A) high-signal questions to interrogate a change, (B) how to write comments people act on.

## A. Prompt patterns (apply to the whole diff or a tricky hunk)

Use these as thinking probes — or fan them out as separate `delegate_work` lenses for a max-effort review.

1. **Top-3 risks.** "What are the three things most likely to break or be exploited in this change?" Forces prioritization over a flat list.
2. **10× scale.** "What breaks first if traffic / data / users grow 10×?" Surfaces N+1s, unbounded memory, missing pagination, hot locks.
3. **First-principles / blank-slate.** "Ignore how it's written — what's the simplest correct design for this problem? How far is the PR from that?" Catches over-engineering and wrong abstractions.
4. **Root-cause (bug-fix PRs).** "Does this fix the *cause* or just the *symptom*? What class of bug does this leave unaddressed?" Demand a regression test that fails on the old code.
5. **Adversary pass.** "I'm a malicious user. Walk every input from the boundary to a sink — where's the unchecked one?" (Pair with `security_review.md`.)
6. **Failure-mode pass.** "For each external call / I/O / await: what happens on timeout, partial write, retry, or crash mid-operation?" Surfaces missing idempotency and error handling.
7. **Future-maintainer pass.** "Six months from now, someone changes the line above this. What silently breaks?" Tests hidden coupling and missing tests.
8. **Diff-vs-description pass.** "Does the code do exactly what the PR says — no more (scope creep), no less (TODO left)?"

## B. Comment craft — make feedback land

**Anatomy of a good review comment:**
```
[severity] file:line — <what> + <why it matters> + <suggested direction>
```
- Always include the **WHY**. "Change this" teaches nothing and invites pushback; "this re-fetches on every render → wrap in useMemo" is actionable.
- **Cite location** with `file_path:line_number`. Quote the offending snippet when it helps.
- **Suggest, don't dictate** — offer a direction or a code suggestion, leave room for the author's judgment on 🟡/🟢.
- **Label severity** (🔴/🟡/🟢/💙) and prefix optional items with `Nit:`. Personal preference ≠ blocker.
- **Ask, when unsure.** "Is `userId` guaranteed non-null here? If not, this NPEs." beats a wrong accusation.
- **Batch related nits** instead of 20 separate threads.
- **Praise specifically.** "💙 nice — extracting `validate()` made this testable" reinforces the behavior you want repeated.

**Tone:** critique the code, not the coder. "This function does X" not "you always do X". Assume competence and good intent.

**Disagreement protocol (don't leave a PR stuck):**
1. Re-state your concern with the technical fact behind it.
2. If still split → quick sync call, then **record the decision in the PR thread**.
3. Still unresolved → escalate to tech lead / maintainer. Net-positive changes shouldn't rot in review limbo.

**Self-check before posting the review:**
- [ ] Did I read the PR description and understand the intent?
- [ ] Did I read every changed (human-written) line, in context?
- [ ] Is every finding labeled by severity?
- [ ] Did I explain WHY for each, with file:line?
- [ ] At least one 💙 if the PR deserves it?
- [ ] Verdict consistent with findings (no 🔴 ⇒ LGTM-able)?
- [ ] Am I blocking only on real issues, not personal preference?
