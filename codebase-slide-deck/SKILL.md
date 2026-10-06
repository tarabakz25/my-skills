---
name: codebase-slide-deck
description: Create slide decks from a local codebase by inspecting architecture, flows, modules, APIs, data models, tests, and implementation details, then turning findings into a presentation outline and editable PPTX. Use when Codex is asked to make slides, a presentation, a PowerPoint, an architecture deck, onboarding deck, technical walkthrough, design review deck, code explanation deck, refactor proposal deck, or Japanese requests such as コードベースからスライド資料を作成, 技術説明資料, 設計共有資料, or PPTX化.
disable-model-invocation: true
---

# Codebase Slide Deck

## Overview

Use this skill to turn repository evidence into a clear technical slide deck. It covers the codebase investigation and narrative shaping steps; when a `.pptx` or rendered deck is required, also use the `Presentations` skill for authoring, export, and visual QA.

## Workflow

1. Clarify the deck target only when it changes the investigation path: audience, purpose, desired slide count, output format, and whether the user wants Japanese or English. If unspecified, infer from the request and repository.
2. Inspect the repository before outlining. Prefer `rg`, `rg --files`, dependency manifests, README/docs, route definitions, schema files, tests, configuration, and entry points.
3. Build an evidence map with file paths and short findings. Keep claims traceable to code, docs, or tests; mark uncertain behavior as inferred.
4. Decide the deck type:
   - `architecture overview`: system boundaries, major modules, data/control flow, runtime/deployment shape.
   - `onboarding walkthrough`: repository map, local setup, key workflows, where to change common behavior.
   - `feature deep dive`: user journey, entry points, service/model interactions, edge cases, tests.
   - `design or refactor proposal`: current pain, evidence, options, recommendation, migration and risk.
   - `incident or bug explanation`: symptom, root cause path, fix, validation, prevention.
5. Draft slide specs before making slides. Each spec should include the slide job, main message, evidence source paths, visual form, and speaker-note-worthy details.
6. Convert implementation detail into visual explanation. Prefer diagrams, flow maps, module maps, sequence charts, tables, and annotated snippets over raw bullet lists.
7. If creating slide code and the user has explicitly allowed subagents/delegation/parallel agent work, split independent slide groups across subagents. Keep narrative, shared design contract, final integration, export, and QA in the main agent.
8. If creating a PowerPoint, invoke `Presentations` after the slide specs are ready. Pass the narrative, slide list, source evidence, required language, and any template/brand constraints.
9. Verify the finished deck against repository facts. Re-check any slide claim that names a module, endpoint, schema, CLI command, environment variable, dependency, metric, or test result.

## Investigation Checklist

Capture only what supports the deck goal:

- Entry points: application bootstrap, routes/pages/controllers, CLI commands, jobs, workers, scheduled tasks.
- Architecture: package/module boundaries, shared libraries, service layers, adapters, external integrations.
- Data: schemas, migrations, ORM models, API contracts, validation, state management, caching.
- Flow: primary user or system journeys, async work, failure paths, permissions, observability.
- Quality: tests, fixtures, CI, lint/type checks, known gaps, TODOs, brittle areas.
- Operations: environment variables, deployment config, build scripts, runtime dependencies.

For large repositories, sample strategically: start from manifests and entry points, then follow only the paths needed for the deck's thesis.

## Slide Planning

Use `references/codebase-deck-patterns.md` when choosing deck structure, diagram types, or slide-by-slide patterns.

Every slide spec should be compact:

```text
slide:
  title:
  job:
  mainMessage:
  evidence:
    - path:line or path
  visual:
  notes:
```

Keep code snippets short and purposeful. A snippet belongs on a slide only if the exact code shape matters; otherwise translate it into a diagram or table and keep the file path in notes.

## Parallel Slide Code Authoring

When the task requires writing slide code and subagents are permitted by the user, parallelize implementation after the narrative, evidence map, slide specs, and design contract are stable.

Use this division of responsibility:

- Main agent: owns repository investigation, deck thesis, slide order, shared visual system, data/evidence accuracy, final file integration, export, rendered QA, and final response.
- Subagents: each owns a bounded, non-overlapping slide range or section. Tell them they are not alone in the codebase and must not revert or overwrite others' edits.

Give each subagent a self-contained brief:

```text
Implement slides N-M only.
Use this shared deck contract: [palette, typography, layout rules, component conventions].
Use these slide specs: [titles, jobs, messages, evidence paths, visual forms].
Write only in [assigned file/path or exported component names].
Do not change shared runtime/export code unless explicitly assigned.
Return changed paths and any assumptions.
```

Prefer disjoint write scopes such as one file per slide section or clearly named component ranges. If the presentation tool requires one integrated source file, have subagents draft section components or slide snippets in separate files, then let the main agent merge them.

After subagents return, review their slide code for:

- Consistency with the shared design contract.
- Correct use of evidence paths and no invented claims.
- No duplicated component names, conflicting imports, or broken export structure.
- Text fit, hierarchy, and slide-specific visual purpose.

Run the normal `Presentations` export and rendered QA only after integration.

## Quality Rules

- Do not invent architecture. Distinguish verified facts from reasonable inference.
- Do not present repository README claims as current truth until the relevant code path is checked.
- Do not turn a codebase tour into a file tree dump. Organize around decisions, flows, and concepts.
- Do not overload slides with raw implementation detail. Put deep specifics into speaker notes or appendix slides.
- Include exact local file references in the working notes so later edits can be traced.
- When dependencies, framework behavior, APIs, pricing, compatibility, or security facts may have changed, verify with official sources before using them.

## Output Expectations

For a deck request, deliver:

- Editable `.pptx` path and preview/render paths from the `Presentations` workflow.
- Brief summary of the deck's narrative and slide count.
- Verification notes: commands or checks run, and any unresolved assumptions.

For an outline-only request, deliver the slide list with evidence paths and recommended visuals.
