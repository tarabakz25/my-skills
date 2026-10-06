# Subagent Orchestration (required)

Code review **must** run through subagents via the `Task` tool. The parent gathers context and synthesizes; it does **not** perform the full review alone.

Why: adversarial verification needs an independent attacker. A subagent is that other party — especially when reviewing your own prior change.

## Rules

1. **Always launch ≥1 review subagent** for a full `/code-review` (not metadata-only, not pure gut-check unless the user asked for gut-check).
2. **Parent does not solitary-review.** Parent may skim the PR description and file list to brief subagents, but findings and adversarial attacks come from subagents.
3. **Own-change second opinion:** if this session (or the same agent) authored the diff, the parent **must not** be the primary reviewer — launch subagent(s) and treat their output as authoritative.
4. **Parallelize** independent lenses in one message (multiple `Task` calls together).
5. **`run_in_background: false`** unless the user asked for background — wait for results before the verdict.
6. **Do not** use `bugbot` / `security-review` Task types unless the user explicitly asked for those product reviews. Default lenses use `generalPurpose`.
7. If `Task` is unavailable or every subagent fails, say so and stop — do **not** silently fall back to a solo confirmation-biased review presented as a full `/code-review`.

## Default launch set

| Subagent | `subagent_type` | Role |
|---|---|---|
| Adversarial reviewer | `generalPurpose` | **Required.** Falsify claims; checklist + correctness; produce Findings + Adversarial verification draft. |
| Security reviewer | `generalPurpose` | **Required** when the diff touches auth, input, data access, I/O, serialization, deps, or network. Otherwise optional. OWASP lens from `security-review.md`. |

Deep / max-effort (optional, add in parallel):
- Correctness / edge-cases lens
- First-principles / over-engineering lens

## Briefing template (every subagent prompt)

Include all of the following so the subagent does not need parent chat history:

```
You are an independent code reviewer. Assume the change may be wrong.
Do not defend the author's story — try to falsify it.

Repo: <absolute path>
Scope: <PR URL | branch | "uncommitted changes" | commit range>
PR title/body: <paste or summarize from gh pr view>
Changed files: <list>
How to get the diff: <e.g. gh pr diff N -R owner/repo | git diff main...HEAD>

Follow the code-review skill contract:
- Severity tags: 🔴 Blocking / 🟡 Should-fix / 🟢 Nit / 💙 Praise
- Read PR intent first, then full-file context (not diff-only)
- Walk review-checklist dimensions relevant to your lens
- Run adversarial verification: extract claims → invert → counterexamples → attack tests-as-proof
- Cite file:line; explain WHY; suggest a direction

Your lens for this run: <adversarial-correctness | security | ...>

Return ONLY:
## Adversarial verification
## Findings (tagged)
## Lens verdict note (1–3 sentences)
Do not write the final merged Verdict — the parent synthesizes.
```

Point subagents at skill reference paths when useful:
- `~/.cursor/skills/code-review/references/adversarial-verification.md`
- `~/.cursor/skills/code-review/references/review-checklist.md`
- `~/.cursor/skills/code-review/references/security-review.md`

## Parent synthesis

After all subagents return:

1. Deduplicate findings (same issue once; keep strongest severity).
2. Merge adversarial sections: union of claims attacked; prefer concrete falsifications over vibes.
3. Resolve conflicts: if one subagent LGTMs and another has 🔴, the 🔴 wins until addressed.
4. Emit the skill **Output Format** (Summary / Adversarial verification / Findings / Verdict) once.
5. Add 💙 if subagents omitted praise but something clearly deserves it (parent may add praise only — not new speculative blockers).

## Quick gut-check exception

When the user asked only for a quick gut-check: still launch **one** adversarial `generalPurpose` subagent with a short prompt (top 3 risks + invert main claim). Parent may not skip the subagent.
