---
name: solo-sdd
description: >-
  Provides lightweight solo SDD with a dedicated branch per spec:
  /solo-sdd brief → specs/{id}/brief.md only; /solo-sdd create → brief.md +
  design.md; /solo-sdd design → design from brief; /solo-sdd build → implement
  the whole spec in the current checkout and open one PR; mid-build
  discoveries/issues → note.md deploy notes. Use for /solo-sdd, brief-only,
  small–medium SDD, note.md, deploy notes, or instead of heavy cc-sdd.
disable-model-invocation: true
version: 3.8.0
---

# Solo SDD

## Overview

Pin intent in a short **brief**, turn it into a **design + tasks**, then ship
one PR per spec (the whole `specs/{id}`) from the current checkout and its
dedicated `sdd/{id}` branch. Use **brief** when you only want intent pinned;
use **create** when you want brief + design in one go. Mid-build discoveries,
problems, or deploy-relevant findings go in optional **`note.md`** — do not
inflate brief/design with ops chatter. Optimized for small–medium solo work —
not cc-sdd / heavy SPEC-NNN pipelines.

Every spec starts on a new `sdd/{id}` branch created from its intended base
branch before any spec file is written. Never write a spec or implementation
on the base branch.

Invariant: **if it is not in brief/design, do not build it; if it is, prove Done when / Verification.**

## When to Use

**Use when:**
- User invokes `/solo-sdd`, `/solo-sdd brief {feature}`, `/solo-sdd create {feature}`, `/solo-sdd design`, or `/solo-sdd build`
- Starting a feature that needs a thin written plan before coding
- Pinning intent only (`brief`) before deciding approach
- Wanting SDD without oversized templates or multi-round review theater
- Capturing deploy notes or mid-build discoveries in `note.md`

**Don't use for:**
- One-line bugfixes with obvious correct behavior
- Pure refactors with no behavior change
- Large multi-team programs that need full system/API catalogs (use a heavier process)

## Command Interface

| Command | Action |
|---------|--------|
| `/solo-sdd` | Help + list `specs/*/` |
| `/solo-sdd brief {feature}` | Create a dedicated branch, then write `brief.md` only |
| `/solo-sdd create {feature}` | Create a dedicated branch, then write `brief.md` + `design.md` |
| `/solo-sdd design {id}` | (Re)write `design.md` from the existing brief in the current checkout |
| `/solo-sdd build {id}` | Implement **entire design** → one PR; write/update `note.md` if discoveries or deploy-relevant issues arise |
| `/solo-sdd status {id}` | Brief/design/tasks + `note.md` (if any) + open PRs for this feature |

**Args:**
- `{feature}` — lowercase kebab-case slug (`payment-retry`)
- `{id}` — full dir name (`20260711-payment-retry`) or unique slug suffix

**Artifacts under `specs/{id}/`:**
- `brief.md` — required from `brief` or `create`
- `design.md` — required before build (`create` writes it, or `/solo-sdd design` after `brief`)
- `note.md` — optional; create only when there is something to record (deploy notes, discoveries, issues). Do **not** create an empty file at `brief` / `create`.

**PR granularity:** one spec = one PR. Do not open one PR per Task. Escape hatch only if the user **explicitly** asks to build a task subset (`Tn…`).

### Resolve id → directory

```bash
ID="<id>"   # e.g. 20260711-payment-retry
ls -d specs/*"${ID}"* 2>/dev/null | head -5
```

Zero matches → list `specs/` and stop. Multiple → ask for full `yyyymmdd-…` prefix.

### List features

```bash
find specs -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort
```

---

## Shared: current checkout + base branch

All commands and writes happen in the current checkout, but each spec gets its
own branch named `sdd/{id}`. Do not create another checkout for Solo SDD. Do
not write a spec or implementation on the base branch.

Resolve the PR base from the user-specified branch, otherwise the repository
default (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`),
otherwise `main`/`master`. The base branch must exist locally; do not silently
use an arbitrary current branch as the base.

Before `/solo-sdd brief` or `/solo-sdd create`:

1. Require a clean worktree (`git status --short` is empty). Do not stash or
   commit unrelated changes on the user's behalf.
2. Resolve `ID` and `BRANCH="sdd/${ID}"`.
3. If the current branch is already `BRANCH`, continue only if the user is
   intentionally resuming that spec. If the current branch is the resolved
   base, create `BRANCH` from it. If the current branch is any other branch,
   stop and ask whether it is the intended base; never branch silently from
   an unrelated branch.
4. If `BRANCH` already exists and is not the current branch, stop and ask
   whether to reuse it. Do not delete or reset an existing branch
   automatically.

---

## Shared: start feature (path + brief)

Used by `/solo-sdd brief` and `/solo-sdd create`.

### 1) Path and branch

```bash
ID="$(date +%Y%m%d)-${FEATURE}"
DIR="specs/${ID}"
BRANCH="sdd/${ID}"
```

If `specs/${ID}` already exists, stop and ask: reuse, bump date, or new slug.
If `BRANCH` already exists and is not the current branch, stop and ask whether
to reuse it. Otherwise, create the branch from the resolved base before
writing any spec file. `BASE` is the resolved base branch from the previous
section; if the current branch is already `BRANCH`, skip the switch:

```bash
if [ "$(git branch --show-current)" != "$BRANCH" ]; then
  git switch -c "$BRANCH" "$BASE"
fi
```

All subsequent writes happen on `BRANCH` in the current checkout. Report the
base and feature branch in the result.

```bash
mkdir -p "$DIR"
```

### 2) Gather (only missing pieces)

Do not re-ask what is already in the conversation or codebase. Fill gaps in one batch:

1. Background (why this spec exists — context / problem)
2. Goal (outcome, not implementation)
3. In / out of scope
4. Success criteria (testable)
5. Hard constraints (platform, time, deps)

If the user says "up to you", assume and label assumptions under **Constraints / notes**.

### 3) Write `brief.md`

Use this template **verbatim** (same headings, same order). Copy from [references/brief-template.md](references/brief-template.md):

```markdown
# <title>

## Background

## Goal

## In scope

## Out of scope

## Success criteria

## Constraints / notes
```

Keep it short (roughly ≤80 lines). **Background** = why this spec exists (context / problem), not the solution. No SPEC-NNN tables, no NFR catalogs, no "Excluded Sections" padding.

---

## `/solo-sdd brief {feature}`

Stop after intent is pinned — no `design.md`.

1. Run **Shared: start feature** (path, branch, gather, write `brief.md`).
2. Commit brief only on `BRANCH`:

```bash
git add "${DIR}/brief.md"
git commit -m "docs(sdd): add ${ID} brief"
```

Do **not** write `design.md` or open a PR.

3. Report:
- `{id}`, spec path (`${DIR}`), base branch, and feature branch (`${BRANCH}`)
- 2–3 line summary of Goal / In scope
- next step: `/solo-sdd design {id}` (then `/solo-sdd build {id}`)

---

## `/solo-sdd create {feature}`

Brief + design in one pass (default when approach is already clear).

1. Run **Shared: start feature** (path, branch, gather, write `brief.md`).
2. Write `design.md` (same rules as `/solo-sdd design` below). Pause only if the brief is still ambiguous — ask one clarifying question, then continue.
3. Commit both on `BRANCH`:

```bash
git add "${DIR}/brief.md" "${DIR}/design.md"
git commit -m "docs(sdd): add ${ID} brief and design"
```

Do **not** open a PR yet.

4. Report:
- `{id}`, spec path (`${DIR}`), base branch, and feature branch (`${BRANCH}`)
- 2–3 line summary
- next step: `/solo-sdd build {id}` (continue on the same branch)

---

## `/solo-sdd design {id}`

Resolve `BRANCH="sdd/${ID}"` from the spec id before reading or writing. Require
the current branch to be `BRANCH`; if it is the base branch or another feature
branch, stop and tell the user to switch to the spec branch. Never create or
refresh a design on the base branch.

Read the current checkout's `brief.md` + codebase and rewrite or refresh `design.md`. Do not invent scope absent from the brief — update the brief first if scope changed.

If `design.md` is missing (after `/solo-sdd brief`), create it. Use this template **verbatim**. Copy from [references/design-template.md](references/design-template.md):

```markdown
# Design: <title>

## Approach （境界・主要フロー・触るモジュール）

## Decisions

- D1: ...

## Tasks

### T1: <title>

- Files: ...
- Done when: ...
- Depends: —

### T2: ...

- Depends: T1

## Verification

- [ ] unit / e2e / manual
```

**Design rules:**
- **Approach**: boundaries, main flow, modules to touch — enough to implement, not a system design doc.
- **Decisions**: only real choices (D1, D2…). Skip empty ceremony.
- **Tasks**: implementation checklist for **one** PR (the whole spec). Each has `Files`, `Done when`, `Depends` (`—` or `Tn`). Not one PR per Task.
- Prefer few tasks (often 1–5). Merge tiny steps; use Depends for order within the PR.
- **Verification**: replace the placeholder with concrete unit / e2e / manual checks tied to Success criteria.

Commit design updates on the same branch when they matter for build/PR:

```bash
git add "${DIR}/design.md"
git commit -m "docs(sdd): add ${ID} design"
```

(Use `update` in the message when refreshing an existing design.)

---

## `/solo-sdd build {id}`

Implement the **entire design** (all Tasks, respecting Depends order) in the
current checkout and **one PR**. Do not open a PR per Task.

### 0) Select work unit

1. Resolve `BRANCH="sdd/${ID}"` and require the current branch to be `BRANCH`. If the current branch is the base branch or another feature branch, stop before changing files and tell the user to switch to the spec branch.
2. Read `brief.md` + `design.md` from the current checkout. If `design.md` is missing, stop and run `/solo-sdd design {id}` first (or tell the user). Also read `note.md` if it exists (prior deploy notes / open issues).
3. Default work unit = **all unfinished tasks** in Depends order.
   - Escape hatch: only if the user explicitly names `Tn…`, implement that subset (all Depends must be done or included) — still one PR for that request, but prefer whole-spec builds.
4. Confirm base for the PR matches the branch’s intended merge target (same resolve-base rule as create) and that the PR head is `BRANCH`.

### 1) Implement

- Cover every selected task's `Files` / `Done when` (default: all tasks).
- Match **Decisions**; if blocked, add `Dn` to design and ask — do not silently expand Out of scope.
- Run Verification checks before PR.
- Commit on the current branch with clear messages (Conventional Commits if the repo uses them). Multiple commits per task are fine; still one PR.

### 1b) Write / update `note.md` (when needed)

If during implementation you hit a **discovery**, **problem**, or **deploy-relevant** finding (migration order, env vars, feature flags, rollback, manual steps, known gaps), record it in `specs/{id}/note.md`. Do not dump this into brief/design unless it changes scope or Decisions — then update those too.

- Create the file only when there is content; skip if nothing to note.
- Use this template **verbatim** on first create. Copy from [references/note-template.md](references/note-template.md):

```markdown
# Notes: <title>

## Deploy notes

- ...

## Discoveries / issues

- YYYY-MM-DD: ...
```

**Note rules:**
- **Deploy notes**: what operators / future-you must do or know to ship or run this (env, migrate, flag, order, rollback). Bullet list; keep short.
- **Discoveries / issues**: dated bullets for surprises, blockers, workarounds, or follow-ups that are not (yet) scope changes.
- Append new dated lines under Discoveries / issues; do not rewrite history away.
- If a discovery becomes real scope → update brief/design, then optionally leave a one-line pointer in notes.

Commit `note.md` with the feature work when it exists (same PR). Spec + code live on the same current branch, so the PR includes both.

### 2) Mark progress

In `design.md`, tick completed tasks (e.g. add `✅` to the `### Tn` heading or a one-line status). Tick Verification items that are now true.

Prefer ticking **before** the final push/PR so the PR includes progress marks. If that commit already shipped, note remaining ticks in the report only.

### 3) Open PR

Push and open **one** PR into **base** (or user-specified branch). Prefer `create-github-pr` / `gh pr create`.

**Title** (verbatim pattern): `{GENRE}: {feature}` — `GENRE` is uppercase (`FIX`, `FEAT`, `CHORE`, …); `{feature}` is a short English phrase (often the slug in words).

Examples: `FEAT: payment retry`, `FIX: session cookie race`, `CHORE: bump sdd tooling`

**Body:** use this template **verbatim** (same headings, same order). Copy from [references/pr-template.md](references/pr-template.md):

```markdown
## Summary

### What

- ...

### Why

- ...

### Spec

- Brief: `specs/{id}/brief.md`
- Design: `specs/{id}/design.md`
- Notes: `specs/{id}/note.md`

## Test

### How to test

- [ ] ...

### Captures

- ...

## Deploy Notes

- None
```

**PR body rules:**
- **What**: what shipped (tasks / behavior), 1–3 bullets
- **Why**: motivation from brief Goal / Background
- **Spec**: link brief + design; include Notes only when `note.md` exists (omit that bullet otherwise)
- **How to test**: concrete steps from Verification / Success criteria; mark only what was actually run
- **Captures**: screenshots, log snippets, or command output worth review — or `None`
- **Deploy Notes**: from `note.md` Deploy notes, or `None`
- Prefer writing the body to a temp file and `gh pr create --body-file` to avoid shell escaping issues

```bash
git push -u origin HEAD
gh pr create --base "${BASE}" --title "${GENRE}: ${FEATURE_EN}" --body-file /tmp/sdd-pr-body.md
```

Report PR URL.

If the whole spec shipped, say so. If an explicit subset was built, suggest `/solo-sdd build {id}` for the remainder (still aiming for one remaining PR when practical).

---

## `/solo-sdd status {id}`

Summarize from the current checkout. Include Background (1–2 lines), Goal, whether `design.md` exists (if not → next: `/solo-sdd design {id}`), task Done/Depends graph when design exists, the current branch's open PRs, remaining Verification, and — if `note.md` exists — a short Deploy notes / open issues blurb.

---

## Anti-bloat (vs cc-sdd)

| Do | Don't |
|----|--------|
| brief + design only (+ `note.md` when needed) | Multi-type template catalogs, SPEC-NNN matrices |
| Ask only missing questions | Long clarification checklists by default |
| Specs in the current checkout on a dedicated `sdd/{id}` branch; 1 PR per spec | Spec on the base or an unintended branch; one PR per Task |
| `brief` when intent-only; `create` when approach is clear | Forcing design before Goal/Success criteria are solid |
| Short Approach + Decisions | Full NFR / glossary / excluded-section padding |
| Keep the current checkout and branch explicit | Hide the branch or PR target |
| Deploy / discovery chatter in `note.md` | Padding brief/design with ops digressions |

---

## Common Pitfalls

- Writing design before the goal/success criteria are clear → use `/solo-sdd brief` (or fix brief) first.
- Tasks without `Done when` → not buildable; fix design.
- Writing artifacts or implementation on the base or an unintended branch → stop, switch to `sdd/{id}`, and confirm the base before starting.
- Running `brief`/`create` with unrelated uncommitted changes → stop; do not stash or commit them automatically.
- Building without `design.md` after brief-only → run `/solo-sdd design {id}` first.
- Opening one PR per Task → wrong; ship the whole spec in one PR unless the user explicitly requests a subset.
- Expanding scope mid-build without updating brief/design.
- Stuffing deploy notes into brief/design — use `note.md` instead (and update brief/design only when scope or Decisions change).
- Creating empty `note.md` at brief/create time — only write it when there is content.

## Verification Checklist

- [ ] `/solo-sdd brief` commits `brief.md` only; does not write `design.md`
- [ ] `specs/yyyymmdd-{feature}/brief.md` uses the verbatim brief headings
- [ ] `design.md` uses the verbatim design headings (including Approach line) — via `create` or `design`
- [ ] Tasks have Files / Done when / Depends
- [ ] `brief`/`create` create `sdd/{id}` from the resolved base before writing files and report both branches
- [ ] Spec commit lands on the dedicated branch; `design`/`build` refuse the base branch; build refuses if `design.md` is missing
- [ ] One PR for the whole spec; title `{GENRE}: {feature}`; body uses verbatim PR headings (Summary/What/Why/Spec, Test/How to test/Captures, Deploy Notes); links `note.md` under Spec when present
- [ ] If mid-build discoveries / deploy-relevant issues occurred → `note.md` exists with Deploy notes and/or dated Discoveries / issues
