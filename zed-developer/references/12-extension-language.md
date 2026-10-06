# Language and language-server extensions

## Layout

```text
extension.toml
languages/<language>/
  config.toml
  highlights.scm
  brackets.scm
  outline.scm
  indents.scm
  injections.scm
  overrides.scm
  textobjects.scm
  redactions.scm
  runnables.scm
  semantic_token_rules.json
Cargo.toml            # only if server integration needs Rust
src/lib.rs
```

Only add query files needed by the grammar/feature.

## Language metadata

```toml
name = "Example"
grammar = "example"
path_suffixes = ["ex"]
line_comments = ["# "]
tab_size = 4
hard_tabs = false
first_line_pattern = "^#!.*\\bexample\\b"
debuggers = ["example-dap"]
```

`name` and `grammar` are required. `path_suffixes` are suffixes, not user-settings globs. `debuggers` controls preference/order in New Process UI.

Register a pinned grammar revision:

```toml
[grammars.example]
repository = "https://github.com/example/tree-sitter-example"
rev = "<full-commit-sha>"
```

Use a full immutable revision for reproducibility. `file://` grammar repository is for local development only; do not publish it.

## Tree-sitter query responsibilities

- `highlights.scm`: canonical Zed captures such as `@keyword`, `@string`, `@type`, `@variable.parameter`.
- `brackets.scm`: `@open`, `@close`; optional rainbow exclusion predicate.
- `outline.scm`: `@item`, `@name`, context/annotation captures.
- `indents.scm`: `@indent`, `@end`.
- `injections.scm`: `@injection.language`, `@injection.content`.
- `overrides.scm`: scoped language setting overrides; understand exclusive vs `.inclusive` ranges.
- `textobjects.scm`: function/class/comment around/inside captures for Vim.
- `redactions.scm`: `@redact` for sensitive syntax nodes.
- `runnables.scm`: `@run`; other non-underscore captures become `ZED_CUSTOM_*` variables.

Compile/test queries against the exact pinned grammar. Node names change across grammar versions. Start with representative fixtures including malformed/incomplete syntax.

## Language server manifest and API

```toml
[language_servers.example-language-server]
name = "Example Language Server"
languages = ["Example"]
```

Names in `languages` must match `config.toml` `name`. Optional language ID mappings use current manifest syntax; verify underscore/hyphen table spelling in current docs because old examples vary.

Implement `language_server_command`, and optionally initialization/workspace configuration and completion/symbol labels. Resolve executable using Worktree APIs and current platform. Return `zed::Command` with command, args, env. Provide useful failures for missing binary, unsupported platform, download failure, and incompatible version.

## Semantic tokens

Place `semantic_token_rules.json` beside `config.toml`. User rules have higher precedence. Test `off`, `combined`, and `full`; ensure the extension is still legible with Tree-sitter only.

## Test matrix

- file detection: suffix, special filename, shebang,
- highlights on valid/incomplete/nested syntax,
- brackets/indent/outline/injections/text objects/runnables,
- server found on PATH and downloaded fallback,
- all supported OS/architectures,
- initialization and workspace settings,
- completion/diagnostics/format/rename,
- offline and denied-capability behavior,
- project trust and remote/container execution.

Official source: [Language Extensions](https://zed.dev/docs/extensions/languages).
