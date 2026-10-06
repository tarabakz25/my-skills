# Recipes

These are starting points, not drop-in replacements. Merge into existing files.

## Comfortable cross-platform appearance

```jsonc
{
  "theme": { "mode": "system", "light": "One Light", "dark": "One Dark" },
  "buffer_font_family": ".ZedMono",
  "buffer_font_size": 14,
  "buffer_line_height": "standard",
  "ui_font_size": 16,
  "terminal": { "font_family": ".ZedMono", "font_size": 14 }
}
```

## Language-server order with explicit default preservation

```jsonc
{
  "languages": {
    "Ruby": {
      "language_servers": ["ruby-lsp", "!solargraph", "!kanayago", "..."]
    }
  }
}
```

Verify actual registered names and default-disabled servers for current extension/version.

## Safe current-file task

```jsonc
[
  {
    "label": "show current file metadata",
    "command": "stat",
    "args": ["$ZED_FILE"],
    "reveal": "always",
    "hide": "never",
    "save": "none"
  }
]
```

Platform-specific command; choose PowerShell equivalent on Windows. Arguments array protects spaces but not availability.

## Worktree setup hook

```jsonc
[
  {
    "label": "install dependencies in new worktree",
    "command": "npm",
    "args": ["ci"],
    "cwd": "$ZED_WORKTREE_ROOT",
    "hooks": ["create_worktree"],
    "reveal": "no_focus",
    "hide": "on_success"
  }
]
```

Only add after explicit agreement: it executes repository dependencies automatically. Never copy `.env`/credentials by default.

## Context-scoped binding

```jsonc
[
  {
    "context": "Workspace > Editor",
    "bindings": {
      "secondary-k secondary-s": "zed::OpenKeymap"
    }
  }
]
```

Confirm current action identifier; example may conflict with base keymap/chord behavior.

## External formatter

```jsonc
{
  "languages": {
    "JavaScript": {
      "format_on_save": "on",
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      }
    }
  }
}
```

Ensure executable is in the Zed project environment and formatter reads stdin/writes stdout.

## Restricted extension capabilities example

```jsonc
{
  "granted_extension_capabilities": [
    { "kind": "process:exec", "command": "*", "args": ["**"] },
    { "kind": "download_file", "host": "github.com", "path": ["**"] },
    { "kind": "npm:install", "package": "*" }
  ]
}
```

This only illustrates shape; tighten command/path/package to actual needs. Changing global grants can break extensions or widen privilege.
