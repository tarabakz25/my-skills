# Agentflow Diagram

Official: https://mermaid.js.org/syntax/agentflow.html

## When
Agentic workflows: agents, nested flows, tasks/tools, and control vs reference vs failure edges.

## Keyword
`agentflow-beta`

## Syntax

`agentflow-beta` then optional direction: `TB`, `TD`, `BT`, `LR`, `RL`.

Nodes: `id["Label"]` plus `@{ shape: … }` (YAML metadata).

| Shape alias | Meaning | Underlying |
| ----------- | ------- | ---------- |
| `task` | Unit of work | `roundedRect` |
| `tool` | Callable capability | `subroutine` |
| `input` | Data in | `lean-right` |
| `decision` | Branch | `diamond` |
| `refdoc` | Reference material | `lin-doc` |
| `action` | Side effect | `hexagon` |

Canonical Mermaid shape names also work.

| Operator | Semantic |
| -------- | -------- |
| `-->` | Sequence (control/data) |
| `-.-` | Reference (consult; no control) |
| `--x` | Failure path |

Labeled edges: `check -- yes --> ship`. Chains: `a --> b --> c`.

Containers: `flow id["Label"]` … `end` (nestable). Shared top-level nodes: `global` … `end` (no id/label). Collapse: `processing@{ view: "collapsed" }` or `@{ view: collapsed }`.

Rendered metadata keys: `shape`, `label`/`labelType`, `view`, `algorithm` (containers), `curve`/`animate`/`animation` (edges). Convention keys (passed through): `description`, `instruction`, `model`, `params`, `returns`, `value`, `example`, `connectorRef`.

Connectors:

```txt
connector github["GitHub API"]
github@{ protocol: "http", endpoint: "https://api.github.com" }
create["create_issue"]@{ shape: tool, connectorRef: "github.create_issue" }
```

`connectorRef` may be a bare id, `connector.capability`, or URL.

## Example

```mermaid
agentflow-beta TB
  flow reviewer["Review Agent"]
    changes["Gather changes"]@{ shape: input }
    analyse["Analyse diff"]@{ shape: task }
    lint["run_linter"]@{ shape: tool }
    ok["Clean?"]@{ shape: decision }
    changes --> analyse --> lint --> ok
  end
```

## Gotchas
- Beta: keyword `agentflow-beta`; syntax may change incompatibly.
- Prototype keys `__proto__`, `constructor`, `prototype` are stripped from metadata.
- Unknown metadata keys are preserved, not rejected.
