# Swimlanes Diagram

Official: https://mermaid.js.org/syntax/swimlanes.html

## When
Process divided by ownership — who owns each step, not only what happens next.

## Keyword
`swimlane-beta` (new)

## Syntax

Starts with `swimlane-beta`, optional direction (default `TB`).

| Direction | Meaning |
| --------- | ------- |
| `TB` / `TD` | Top to bottom |
| `BT` | Bottom to top |
| `LR` | Left to right |
| `RL` | Right to left |

Top-level `subgraph` … `end` blocks are lanes. Optional id + label: `subgraph sales [Sales team]`.

Nodes and edges use flowchart-style syntax.

| Node | Shape |
| ---- | ----- |
| `id[Text]` | Rectangle (task) |
| `id(Text)` | Rounded |
| `id([Text])` | Stadium (start/end) |
| `id{Text}` | Decision |
| `id((Text))` | Circle |

| Edge | Meaning |
| ---- | ------- |
| `A --> B` | Arrow |
| `A --- B` | Line |
| `A -->|Label| B` | Arrow with label |
| `A -.-> B` | Dotted |
| `A ==> B` | Thick |

Accessibility: `accTitle` / `accDescr` after the keyword.

```txt
swimlane-beta LR
  subgraph Customer
    request[Request service]
  end
  subgraph Support
    triage[Triage request]
  end
  request --> triage
```

## Example

```mermaid
swimlane-beta LR
  subgraph Customer
    request[Request service]
    receive[Receive update]
  end
  subgraph Support
    triage[Triage request]
    answer[Send answer]
  end
  subgraph Engineering
    investigate[Investigate issue]
    fix[Prepare fix]
  end
  request --> triage
  triage -->|Known issue| answer
  triage -->|Needs code change| investigate
  investigate --> fix --> answer
  answer --> receive
```

## Gotchas
- Keyword is `swimlane-beta`; syntax may evolve.
- Only top-level subgraphs become swimlanes.
- Prefer short stable ids; put decisions in the lane that owns them.
