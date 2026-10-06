---
name: mermaid
description: >-
  Writes, edits, and debugs Mermaid diagrams from official mermaid.js.org syntax.
  Use when the user asks for a mermaid diagram, flowchart, sequence/class/state/ER
  diagram, gantt, git graph, mindmap, C4, sankey, pie/xy/radar chart, architecture
  diagram, or a ```mermaid fence; or when a mermaid parse error needs fixing.
  Prefer current https://mermaid.js.org docs over memory.
metadata:
  hermes:
    tags:
      - mermaid
      - diagrams
      - flowchart
      - sequence
      - markdown
      - uml
    related_skills: [presentations, slidev, codebase-slide-deck]
---

# Mermaid

Text-to-diagram syntax. Load this skill as a **router**: pick the diagram type, then read **only** that type's reference. Do not load every reference.

Official intro: https://mermaid.js.org/intro/
Syntax index: https://mermaid.js.org/intro/syntax-reference.html
Live editor: https://mermaid.live

## Workflow

1. Choose the type from the router below (user request wins if they name one).
2. Read `references/common.md` once per task (comments, frontmatter, themes, parse-breakers).
3. Read **one** matching `references/<type>.md`. Load a second only if the first is the wrong type.
4. Emit a fenced `mermaid` block. First non-frontmatter line is the diagram keyword.
5. If the host may not render Mermaid, still emit the fence; mention https://mermaid.live for preview.

Prefer current docs at mermaid.js.org when a flag, shape, or keyword is not in the loaded reference.

## Router

| User intent | Keyword | Load |
|---|---|---|
| Process, decision tree, system flow | `flowchart` | `references/flowchart.md` |
| Messages over time, API/protocol calls | `sequenceDiagram` | `references/sequence.md` |
| Classes, members, UML relations | `classDiagram` | `references/class.md` |
| Finite states and transitions | `stateDiagram-v2` | `references/state.md` |
| Data model, entities, cardinality | `erDiagram` | `references/er.md` |
| SysML requirements | `requirementDiagram` | `references/requirement.md` |
| UML use cases (beta) | `usecase-beta` | `references/usecase.md` |
| Sequence-like with ZenUML syntax | `zenuml` | `references/zenuml.md` |
| Schedule, tasks vs time | `gantt` | `references/gantt.md` |
| Proportions / slices | `pie` | `references/pie.md` |
| Bar or line vs two axes | `xychart` | `references/xy-chart.md` |
| 2×2 priority / fit matrix | `quadrantChart` | `references/quadrant.md` |
| Flow of quantity between nodes | `sankey` | `references/sankey.md` |
| Spider / multi-axis scores (beta) | `radar-beta` | `references/radar.md` |
| Nested proportional rectangles (beta) | `treemap-beta` | `references/treemap.md` |
| Set overlap (beta) | `venn-beta` | `references/venn.md` |
| Chronology by section | `timeline` | `references/timeline.md` |
| Task steps scored by actor | `journey` | `references/user-journey.md` |
| Board columns and cards | `kanban` | `references/kanban.md` |
| Git branches / commits | `gitGraph` | `references/gitgraph.md` |
| C4 context/container/component (experimental) | `C4Context` … | `references/c4.md` |
| Cloud/service topology (beta) | `architecture-beta` | `references/architecture.md` |
| Nested layout blocks | `block` | `references/block.md` |
| Network packet bit layout | `packet` | `references/packet.md` |
| Hierarchical brainstorm | `mindmap` | `references/mindmap.md` |
| File/tree outline (beta) | `treeView-beta` | `references/treeview.md` |
| Grammar / railroad syntax (beta) | `railroad-ebnf-beta` | `references/railroad.md` |
| Process by owner/lane (beta) | `swimlane-beta` | `references/swimlanes.md` |
| Agent/tool flow (beta) | `agentflow-beta` | `references/agentflow.md` |
| Wardley map (beta) | `wardley-beta` | `references/wardley.md` |
| Event modeling timeline | `eventmodeling` | `references/eventmodeling.md` |
| Cynefin domains (beta) | `cynefin-beta` | `references/cynefin.md` |
| Fishbone / cause-effect (beta) | `ishikawa-beta` | `references/ishikawa.md` |

Default when the user says "diagram" with no type: **flowchart**. Default for "how these services talk": **sequenceDiagram**. Default for "data model": **erDiagram**.

`*-beta` and C4/sankey syntax may still change. Prefer a stable type unless the user asked for that diagram.

## Output rules

- Wrap in a markdown `mermaid` fence (GitHub, GitLab, many docs tools render it).
- Prefer `flowchart` over legacy `graph`.
- Prefer `stateDiagram-v2` over `stateDiagram`.
- Quote labels that contain reserved words, punctuation, or nested shape characters.
- Keep IDs short (`camelCase` or `snake_case`); put display text in `[]` / quotes.
- One diagram per fence. Do not mix types in one block.

## Common pitfalls

- Lowercase `end` as a node/message can break **flowchart** and **sequence**. Quote or capitalize it.
- Unknown keywords fail parse; misspelled config keys fail silently.
- `%%` comments must not contain `{` `}` (looks like a directive).
- Node id starting with `o` or `x` after `---` can become a circle/cross edge in flowcharts.
- GitHub Flavored Markdown: no spaces on the fence language tag; do not indent the fence as if it were nested code unless required.

## Verification checklist

- [ ] Loaded `references/common.md` plus exactly the matching type file
- [ ] First diagram line is the correct keyword
- [ ] Labels with spaces/`end`/parentheses are quoted
- [ ] Fence is `mermaid`, not `mermaid-example`
- [ ] Beta/experimental types were used only when that type was the right fit
