# Cynefin Framework Diagram

Official: https://mermaid.js.org/syntax/cynefin.html

## When
Place items into Clear / Complicated / Complex / Chaotic / Confusion domains, optionally with domain transitions.

## Keyword
`cynefin-beta`

## Syntax

| Keyword | Role |
| ------- | ---- |
| `cynefin-beta` | Diagram declaration |
| `title` | Optional title |
| `complex` | Complex domain block |
| `complicated` | Complicated domain block |
| `clear` | Clear domain block |
| `chaotic` | Chaotic domain block |
| `confusion` | Confusion / Disorder block |
| `-->` | Transition between two domains |

Items are quoted strings on their own lines inside a domain block.

```txt
complex
  "Investigate root cause"
  "Run chaos experiment"
```

Transitions (top level, optional label):

```txt
complex --> complicated : "Pattern identified"
clear --> chaotic : "Complacency"
```

Domain keywords are fixed; declaration order does not change layout (Complex TL, Complicated TR, Chaotic BL, Clear BR, Confusion center).

Accessibility: `accTitle` / `accDescr`.

Config under `cynefin`: `width`, `height`, `padding`, `showDomainDescriptions`, `boundaryAmplitude`, `seed`.

## Example

```mermaid
cynefin-beta
  title Incident Response
  complex
    "Investigate root cause"
    "Run chaos experiment"
  complicated
    "Analyze performance data"
  clear
    "Restart service"
  chaotic
    "Page on-call immediately"
  confusion
    "Unknown failure mode"
  complex --> complicated : "Pattern identified"
  clear --> chaotic : "Complacency"
```

## Gotchas
- Only the five domain keywords are recognized.
- Confusion shows at most 3 items (`+N more` after that).
- Self-loop transitions (`complex --> complex`) are ignored.
- Handdrawn mode is not supported.
