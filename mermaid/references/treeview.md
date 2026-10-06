# TreeView

Official: https://mermaid.js.org/syntax/treeView.html

## When
Directory-like hierarchies with optional icons, highlights, and inline descriptions (v11.14.0+).

## Keyword
`treeView-beta`

## Syntax

Structure from indentation or box-drawing characters (auto-detected). Labels may be bare or quoted (spaces).

| Rule | Effect |
| --- | --- |
| Trailing `/` | Directory — bold label |
| Quoted `"my file"` | Spaces / special names |
| `%% comment` | Invisible comment |

```
treeView-beta
    my-project/
        src/
            index.js
        package.json
```

### Box-drawing input

Supports `├──` `└──` `│` and heavy `┣━━` `┗━━` `┃`. Depth = column of the branch character. Tabs expand to spaces.

```
treeView-beta
├── src/
│   ├── index.ts
│   └── utils.ts
└── README.md
```

### Annotations (any order, combinable)

| Annotation | Effect |
| --- | --- |
| `:::highlight` (or other class) | CSS class; built-in `highlight` |
| `## description` | Italic description beside label |
| `icon(pack:name)` | Explicit icon (always shown) |
| `icon()` / `icon(none)` | Hide icon when `showIcons` is on |

```
App.tsx :::highlight icon(logos:react) ## main component
```

### Icons config

Icons off by default. Enable built-in `file`/`folder` with:

```
---
config:
  treeView:
    showIcons: true
---
```

Optional maps (registered icon packs): `filenameIcons`, `extensionIcons`, `defaultIconPack`. Unprefixed `icon(rust)` resolves via `defaultIconPack`. Value `none` hides matching file-type icons.

### Useful config

| Property | Default | Role |
| --- | --- | --- |
| `rowIndent` | 10 | Per-level indent |
| `showIcons` | false | Built-in file/folder icons |
| `defaultIconPack` | `''` | Resolve unprefixed icons |
| `filenameIcons` / `extensionIcons` | `{}` | File-type icon maps |

## Example

```mermaid
treeView-beta
    my-project/
        src/
            App.tsx :::highlight icon(logos:react) ## main component
            index.js ## entry point
        .env ## environment variables
        Dockerfile
        package.json
```

## Gotchas

- Built-in icons stay hidden unless `showIcons: true`; explicit `icon(...)` still renders.
- Icon packs must be registered by the host; unknown icons show as `?`.
- Parse error line numbers refer to original input (after tab expansion).
