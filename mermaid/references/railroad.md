# Railroad Diagram

Official: https://mermaid.js.org/syntax/railroad.html

## When
Syntax / grammar diagrams (Wirth-style railroad) from EBNF, ABNF, PEG, or IR constructors (v11.16.0+).

## Keyword

| Type | Keyword | Notation |
| --- | --- | --- |
| EBNF | `railroad-ebnf-beta` | W3C / ISO 14977 EBNF |
| ABNF | `railroad-abnf-beta` | RFC 5234 |
| PEG | `railroad-peg-beta` | Parsing Expression Grammar |
| IR | `railroad-beta` | Explicit constructors |

## Syntax

Shared outer shape:

1. Diagram keyword on first line
2. Optional `title`, `accTitle:`, `accDescr:`
3. One rule per statement, each ending with `;`

### EBNF (`railroad-ebnf-beta`)

Assignment: `name = definition ;` (also `::=`).

| Feature | W3C | ISO 14977 |
| --- | --- | --- |
| Terminal | `"t"` / `'t'` | same |
| Non-terminal | `identifier` | same |
| Sequence | `A B` | `A , B` |
| Choice | `A \| B` | `A \| B` |
| Optional | `A?` | `[ A ]` |
| Repeat 0+ | `A*` | `{ A }` |
| Repeat 1+ | `A+` | — |
| Group | `( A B )` | `( A B )` |
| Comment | `/* t */` | `(* t *)` |
| Special | — | `? text ?` |
| Exception | `A - B` | `A - B` |

### ABNF (`railroad-abnf-beta`)

`name = definition ;` — alternation `/`; concat by space; reps `*A`, `1*A`, `2*4A`, `3A`; optional `[ A ]`; terminals `"text"` or `%x41` / `%d65` / `%b...` (ranges `%x30-39`); comments `;` to EOL.

### PEG (`railroad-peg-beta`)

`Name <- definition ;` — ordered choice `/`; suffix `?` `*` `+`; predicates `&A` `!A`; `.` any char; comments `#` to EOL.

### IR (`railroad-beta`)

| Constructor | Meaning |
| --- | --- |
| `terminal("text")` | Literal |
| `nonterminal("name")` | Rule ref |
| `sequence(a, b, ...)` | Concat |
| `choice(a, b, ...)` | Alternatives |
| `optional(a)` | Zero or one |
| `zeroOrMore(a)` / `oneOrMore(a)` | Repetition |
| `special("text")` | Special sequence |

## Example

```mermaid
railroad-ebnf-beta
title "Digit Definition"

digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
```

## Gotchas

- Every rule must end with `;`.
- Stick to one notation/keyword per diagram.
- `handDrawn` look is not supported for railroad diagrams.
- ABNF comments use `;` to end of line — do not confuse with the required rule-terminating `;`.
