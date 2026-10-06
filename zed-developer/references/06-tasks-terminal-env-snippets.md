# Tasks, terminal, environment, and snippets

## Task scopes

- Global: `~/.config/zed/tasks.json` (Windows uses Zed config under `%APPDATA%`); open with `zed: open tasks`.
- Project: `<worktree>/.zed/tasks.json`; open with `zed: open project tasks`.
- One-shot: entered in task modal; project/session-specific and not persisted.
- Language extensions may expose runnables/tags.

A tasks file is an array:

```jsonc
[
  {
    "label": "test current project",
    "command": "npm",
    "args": ["test"],
    "cwd": "$ZED_WORKTREE_ROOT",
    "env": { "CI": "1" },
    "save": "all",
    "use_new_terminal": false,
    "allow_concurrent_runs": false,
    "reveal": "always",
    "hide": "never",
    "shell": "system",
    "show_summary": true,
    "show_command": true
  }
]
```

Prefer `command` plus `args` over shell interpolation, especially for paths containing spaces. Only put shell syntax in `command` when a shell pipeline/loop is truly needed. Never interpolate untrusted selected text into a shell command.

## Variables

Common variables include `ZED_FILE`, `ZED_FILENAME`, `ZED_DIRNAME`, `ZED_RELATIVE_FILE`, `ZED_RELATIVE_DIR`, `ZED_STEM`, `ZED_ROW`, `ZED_COLUMN`, `ZED_SYMBOL`, `ZED_SELECTED_TEXT`, `ZED_LANGUAGE`, `ZED_WORKTREE_ROOT`, and `ZED_MAIN_GIT_WORKTREE`. `${NAME:default}` provides a default. Captures from runnable queries become `ZED_CUSTOM_<CAPTURE>`.

Variables can be used in labels, args, and cwd. If a keybinding reruns a task, `reevaluate_context: true` refreshes context variables.

Hook `create_worktree` can run after a linked worktree is created. Treat hooks as repository code execution and keep them transparent, safe, and idempotent.

## Terminal and environment

How Zed is launched matters:

- CLI launch inherits the invoking shell environment, even if Zed was already running (current documented behavior).
- GUI launch obtains an environment by spawning a login shell in the home directory; projects can receive a project-specific login-shell environment.
- Tasks/terminals combine process, CLI/project, and explicit settings environments with later values overriding earlier ones.
- LSP binary lookup and process environment have their own documented rules; test from the same launch mode.
- SSH/container tasks and terminals run remotely/in the container.

For PATH failures, compare `env`/`PATH` from a Zed terminal with the user's external shell. Check shell startup files for noninteractive/login assumptions, slow output, and commands that print text. Use `direnv`/mise/asdf according to current environment docs; avoid embedding secrets in shared task files.

## Snippets

User snippets live in `~/.config/zed/snippets/` and open via `snippets: open folder`. Language filename is lowercase display name, with documented exceptions such as global `snippets.json`, JSX using `javascript.json`, and Plain Text using `plaintext.json`.

```json
{
  "Log to console": {
    "prefix": "log",
    "body": ["console.info(\"${1:value}\")", "$0"],
    "description": "Log a value"
  }
}
```

Supported documented placeholders include `$1`, `${1:default}`, linked same-number placeholders, and `$0`. Escape a literal dollar. Only JSON snippet files are supported; if prefix is a list, documented behavior uses only the first prefix. Do not promise full VS Code variable/transform compatibility without verification.

Official sources: [Tasks](https://zed.dev/docs/tasks), [Terminal](https://zed.dev/docs/terminal), [Environment](https://zed.dev/docs/environment), [Snippets](https://zed.dev/docs/snippets).
