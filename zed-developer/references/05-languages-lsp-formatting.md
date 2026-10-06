# Languages, LSP, formatting, linting, and semantic tokens

## Responsibility map

- Tree-sitter grammar: parsing, syntax captures, outline, brackets, indentation, injections, text objects, runnables.
- Language server (LSP): diagnostics, completion, definitions, references, rename, formatting, code actions, inlay hints, semantic tokens.
- Formatter: language server, external command, code action, or sequence.
- Toolchain: runtime/compiler/environment selection for supported languages.
- User/project settings: enable/order servers and tune behavior.

Diagnose the correct layer. A wrong syntax color is not automatically an LSP problem; missing completion is not automatically a grammar problem.

## Per-language configuration

```jsonc
{
  "languages": {
    "JavaScript": {
      "tab_size": 2,
      "format_on_save": "on",
      "formatter": [
        { "code_action": "source.fixAll.eslint" },
        {
          "external": {
            "command": "prettier",
            "arguments": ["--stdin-filepath", "{buffer_path}"]
          }
        }
      ]
    }
  }
}
```

External formatters should generally read stdin and write stdout. `{buffer_path}` supplies filename context to tools such as Prettier; do not configure a formatter to directly mutate/read the on-disk file instead of stdin unless current docs explicitly require it.

Selection formatting differs by formatter: LSP range formatting is precise when supported; Prettier can format ranges; generic external commands are skipped; code actions often affect the whole buffer.

## Language-server order

```jsonc
{
  "languages": {
    "PHP": {
      "language_servers": ["intelephense", "!phpactor", "..."]
    }
  }
}
```

- Listed names establish order.
- `!name` disables.
- `...` inserts all remaining registered servers at that position.
- The override replaces the default list. A default-disabled server can be unintentionally re-enabled by `...`; explicitly negate it.
- Omit `...` for a strict allowlist.

## Server-specific configuration

```jsonc
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "check": { "command": "clippy" }
      }
    },
    "tailwindcss-language-server": {
      "settings": {
        "tailwindCSS": { "emmetCompletions": true }
      }
    }
  }
}
```

Use nested objects, not VS Code dotted-key notation. `initialization_options` are sent at startup and need an LSP restart. `settings` may be requested/reloaded at runtime, but actual behavior is server-dependent.

A custom binary shape can include `path`, `arguments`, `env`, and `ignore_system_version`; verify current schema before generating it. Prefer project/toolchain discovery over hardcoded personal absolute paths in shared config.

## File association

```jsonc
{
  "file_types": {
    "TOML": ["MyLockFile"],
    "Dockerfile": ["Dockerfile*"]
  }
}
```

User `file_types` supports glob-like matching. Extension language `config.toml` `path_suffixes` does not; do not conflate them.

## Semantic tokens and inlay hints

- `semantic_tokens`: `off` (Tree-sitter), `combined` (overlay), or `full` (LSP replaces Tree-sitter), at research baseline.
- Style with `global_lsp_settings.semantic_token_rules`; user rules override extension rules, which override built-ins.
- Inlay hints are configured through `inlay_hints` and server-specific options. If enabled but absent, confirm server support and server settings.

## Troubleshooting sequence

1. Confirm Zed recognizes the intended language from the status bar.
2. Check file association and project trust.
3. Inspect Zed log and language server logs/status.
4. Run `editor: restart language server` after startup-option changes.
5. Verify executable from the same environment in which Zed runs (GUI vs CLI, local vs remote/container).
6. Test a minimal project without competing servers.
7. Check formatter directly on stdin and server health.
8. Re-enable components one at a time.

Do not remove all language servers or reinstall Zed before checking environment, project trust, and logs.

Official sources: [Configuring Languages](https://zed.dev/docs/configuring-languages), individual [Languages](https://zed.dev/docs/languages), [Diagnostics](https://zed.dev/docs/diagnostics), [Environment](https://zed.dev/docs/environment).
