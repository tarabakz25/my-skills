# Wardley Maps

Official: https://mermaid.js.org/syntax/wardley.html

## When
Value-chain strategy maps: visibility vs evolution of components.

## Keyword
`wardley-beta`

## Syntax

```txt
wardley-beta
title Optional Title
size [1100, 600]
```

Coordinates are OnlineWardleyMaps `[visibility, evolution]` — **not** (x, y). Visibility 0–1 bottom→top; evolution 0–1 left→right.

| Element | Syntax |
| ------- | ------ |
| Component | `component Name [vis, evo]` |
| Label offset | `… label [offsetX, offsetY]` |
| Anchor | `anchor Name [vis, evo]` |
| Inertia | `(inertia)` after coords |
| Strategy | `(build)` `(buy)` `(outsource)` `(market)` |
| Dependency | `A -> B` or `A --> B` |
| Annotated dep | `A -> B; label` |
| Dashed | `A -.-> B` |
| Flow | `A +> B` / `A +< B` / `A +<> B` / `A +'text'> B` |
| Evolve | `evolve Name targetEvo` |
| Trend | `Component -.- (x, y)` — standard (x,y), not [vis,evo] |
| Note | `note "text" [vis, evo]` (quotes required) |
| Annotations | `annotations [x, y]` then `annotation N,[x, y] "text"` |
| Forces | `accelerator "…" [vis, evo]` / `deaccelerator "…" [vis, evo]` |
| Stages | `evolution A -> B -> C -> D` |
| Dual labels | `evolution Genesis / Concept -> …` |
| Stage widths | `evolution Genesis@0.2 -> Custom@0.4 -> …` |
| Pipeline | `pipeline Parent { component "Name" [evo] … }` |

Hyphenated names need no quotes; quote if the name starts with a non-letter or has grammar-hostile characters.

## Example

```mermaid
wardley-beta
title Tea Shop Value Chain
anchor Business [0.95, 0.63]
component Cup of Tea [0.79, 0.61]
component Tea [0.63, 0.81]
component Hot Water [0.52, 0.80]
component Kettle [0.43, 0.35]
component Power [0.10, 0.70]
Business -> Cup of Tea
Cup of Tea -> Tea
Cup of Tea -> Hot Water
Hot Water -> Kettle
Kettle -> Power
evolve Kettle 0.62
evolve Power 0.89
note "Standardising power allows Kettles to evolve faster" [0.30, 0.49]
```

## Gotchas
- Coords are `[visibility, evolution]`, opposite of typical (x, y). Trends use `(x, y)`.
- Note and annotation text must be in quotes.
- `look: handDrawn` is not supported.
