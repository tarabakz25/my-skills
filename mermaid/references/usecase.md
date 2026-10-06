# Use Case Diagram (beta)

Official: https://mermaid.js.org/syntax/usecase.html

## When
Actors interacting with system use cases (UML use-case view). **Beta** (12.0.0+).

## Keyword
`usecase-beta`

## Syntax

Put each statement on its own physical line. Direction: `direction TD|TB|BT|LR|RL`.

### Actors & use cases
IDs match `[A-Za-z0-9_]+` (may start with a digit). Bare actor uses its id as label.
```
actor Customer
actor Admin("Main administrator")
Login("Sign in")
Report[Generate report]
"Reset password"
```
Ellipse: `Id("label")`. Rectangle: `Id[label]`. Quoted-only `"Reset password"` gets a deterministic id (`Reset_password`). Undeclared relationship endpoints become ellipse use cases; **actors are never inferred** — always declare `actor`.

Actor variants:
```
actor Normal("Normal")
actor Hollow("Hollow")@{ type: hollow }
actor Awesome("Awesome")@{ type: awesome }
actor Icon("Icon")@{ icon: "fa:user" }
actor Sales@{ business: true } <<Employee>>
```
Metadata allows only `type`, `icon`, `business`. Icon cannot combine with non-normal `type` or `business: true`. Stereotype: `<<...>>` after metadata, before `:::class`.

### System boundaries
```
systemBoundary sb1["Payment service"]@{ type: package }:::system
  actor Clerk("Payment clerk")
  Authorize("Authorize payment")
end
```
Default boundary type `rect`; `type: package` adds a title tab. One level deep only — contents are actor/use-case declarations, blanks, and `%%` comments. Relationships stay at top level. An element belongs to at most one boundary.

### Relationships
Solid associations: `-->`, `<--`, `--`, `--o`, `o--`, `--x`, `x--` (optional label: `User -- "label" --> Login`).

UML operators:
```
Checkout ..> : include Payment
ApplyCoupon ..> : extend Checkout
Admin --|> Person
ApplyCoupon --|> Checkout
```
Include/extend require use-case ends. Generalization: two actors or two use cases. Extra dashes lengthen point/markerless solid edges (`-->` / `--->`); put extras on the right of a label: `A -- "longer" ----> B`.

Edge IDs: `Customer opens@-- "starts" ---> Checkout` then `style`/`class`/`@{ animation: fast }`.

### Notes
```
note for Login "`Requires an **active session**`"
note for User "Starts the workflow"
```
One target (actor or use case); no placement side keywords.

Comments: whole-line `%%` only (`//` and `#` are not comments). Semicolon is not a statement separator.

## Example
```mermaid
usecase-beta
direction LR
actor Customer
actor Support
systemBoundary Storefront
  Browse("Browse catalogue")
  Checkout("Checkout")
end
systemBoundary Fulfilment
  Track("Track delivery")
end
Customer --> Browse
Customer --> Checkout
Customer --> Track
Support --> Track
Checkout ..> : include Browse
```

## Gotchas
- Keyword is `usecase-beta` (single token); diagram is beta.
- Actors must be declared with `actor` — never inferred from edges.
- One statement per physical line (except Markdown strings / boundary blocks).
- Boundaries cannot nest; relationships/notes cannot live inside a boundary block.
- `#` / `//` are not comments; use `%%`.
