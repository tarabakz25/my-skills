# Settings

## Select the correct scope

| Scope | Path / mechanism | Use for |
|---|---|---|
| User, macOS | `~/.config/zed/settings.json` | global preferences |
| User, Linux | `${XDG_CONFIG_HOME:-~/.config}/zed/settings.json` | global preferences |
| User, Windows | `%APPDATA%\Zed\settings.json` | global preferences |
| Project | `<project>/.zed/settings.json` | repository-specific editor/language/tooling behavior |
| Nested project | `.zed/settings.json` in a subdirectory | more granular overrides for that subtree |
| Remote server | same user path on remote OS | server-side paths, proxy, remote tooling |
| Release channel | top-level `stable`, `preview`, `nightly` object | per-channel overrides |

Use `zed: open settings`, `zed: open settings file`, `zed: open project settings`, and `zed: open default settings` rather than guessing paths when Zed is available.

The settings file is JSON with `//` comments. Treat it as JSONC. Do not assume arbitrary JSON5 syntax is accepted.

## Layering and merge model

Order: defaults → user → project/nested project. Later layers win. Object properties generally merge, but arrays and specifically documented collection settings can replace rather than append. Before changing an array, read its setting documentation. Important examples:

- `languages.<Language>.language_servers` replaces the default list. Use `"..."` to retain otherwise-unlisted servers and `"!server"` to disable explicitly.
- `file_scan_exclusions` overrides defaults; include desired defaults in the replacement.
- `file_scan_exclusions` wins over `file_scan_inclusions`.
- `.editorconfig` `end_of_line` overrides Zed `line_ending`.
- Some settings are user-only because they affect the whole UI, such as theme or modal editing mode; do not promise every key works in project settings.

## Safe edit protocol

1. Read the complete current target file.
2. Validate its existing syntax before editing; report pre-existing errors separately.
3. Find the canonical setting key and accepted value shape.
4. Determine whether an EditorConfig, language override, nested settings file, release-channel object, remote setting, or CLI environment has higher/effective precedence.
5. Apply an exact minimal edit preserving comments and siblings.
6. Run `scripts/validate_jsonc.py`.
7. State whether a language server, terminal, task, remote connection, or Zed must restart.
8. Give a rollback patch or exact key to remove.

## Useful patterns

Dynamic light/dark theme:

```jsonc
{
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "One Dark"
  }
}
```

Per-language behavior:

```jsonc
{
  "languages": {
    "Python": {
      "tab_size": 4,
      "format_on_save": "on",
      "formatter": "language_server"
    }
  }
}
```

Channel-specific override:

```jsonc
{
  "vim_mode": false,
  "nightly": {
    "vim_mode": true
  }
}
```

Deep link examples: `zed://settings/theme`, `zed://settings/vim_mode`, `zed://settings/buffer_font_size`.

## High-impact settings requiring explicit warning

- `session.trust_all_worktrees`: bypasses per-worktree trust prompts and can allow project settings to install/start language and MCP servers.
- `granted_extension_capabilities`: reducing it can intentionally break extensions; broadening it expands execution/download/install privileges.
- `file_scan_inclusions`, `scan_symlinks: "always"`: can harm performance or traverse unexpectedly large trees.
- `global_lsp_settings.request_timeout: 0`: waits indefinitely.
- custom external formatter commands: execute local binaries; prefer stdin/stdout and arguments arrays where supported.
- `disable_ai`: impacts all native AI functionality.

## Do not guess

For a requested key not covered in these references, use All Settings or the running Zed default settings. Avoid fabricated VS Code-like keys; Zed often uses different names and value shapes.

Official sources: [Configuring Zed](https://zed.dev/docs/configuring-zed), [All Settings](https://zed.dev/docs/reference/all-settings), [Configuring Languages](https://zed.dev/docs/configuring-languages), [Worktree Trust](https://zed.dev/docs/worktree-trust).
