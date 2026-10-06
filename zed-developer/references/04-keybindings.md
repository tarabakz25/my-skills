# Keybindings

## Files and tools

- macOS/Linux: `~/.config/zed/keymap.json`
- Windows: `%APPDATA%\Zed\keymap.json`
- Open: `zed: open keymap file`
- Inspect active context: `dev: open key context view`
- Find canonical actions: Command Palette, All Actions, and default keybindings.

The root is an array. Later matching bindings at the same context level win; more specific/lower context nodes win; user bindings load after built-ins.

```jsonc
[
  {
    "context": "Workspace",
    "bindings": {
      "ctrl-alt-t": "terminal_panel::ToggleFocus"
    }
  }
]
```

Never copy an action name from memory. Confirm exact namespace/casing and argument shape.

## Context expressions

- Boolean: `Editor && mode == full`, `!Editor && !Terminal`
- Alternatives: `Editor || Terminal`
- Hierarchy: `Workspace > Editor`
- Grouping: parentheses
- OS: `os == macos > Editor`

Attributes exist only at their defining tree node. Use the key context view to understand a failing expression.

## Actions and arguments

```jsonc
{
  "bindings": {
    "cmd-1": ["workspace::ActivatePane", 0],
    "ctrl-a": ["pane::DeploySearch", { "replace_enabled": true }]
  }
}
```

Use `null` to unbind a matching action:

```jsonc
{ "context": "Workspace", "bindings": { "cmd-r": null } }
```

## Chords and key syntax

A chord is space-separated: `"cmd-k cmd-s"`. If a shorter binding is also a prefix, Zed waits approximately one second for the next key. Modifiers include `ctrl-`, `cmd-`/`win-`/`super-`, `alt-`, `shift-`, `fn-`, and `secondary-` (Command on macOS, Control on Windows/Linux). Prefer `secondary-` for cross-platform intent when semantics match.

`workspace::SendKeystrokes` has limitations: asynchronous UI transitions do not complete mid-sequence, at most 100 simulated keys, and text may be sent verbatim. Prefer a direct action.

## Base and modal keymaps

Documented base keymaps include VS Code, Atom, Emacs (Beta), JetBrains, Sublime Text, TextMate, Cursor, and None. `None` disables all base bindings. Vim and Helix add modal contexts; a globally convenient key may conflict in insert/normal/select modes. Read the Vim/Helix docs and scope custom bindings.

## Robust response pattern

1. Ask desired key and OS only if not given.
2. Search current keymap for conflicts.
3. Confirm action in current Zed.
4. Use the narrowest context.
5. Add an unbind only if fallback behavior is unwanted.
6. Validate JSONC and explain conflict/debug steps.

Official sources: [Keybindings](https://zed.dev/docs/key-bindings), [All Actions](https://zed.dev/docs/all-actions), [default keymap sources](https://github.com/zed-industries/zed/tree/main/assets/keymaps), [Vim Mode](https://zed.dev/docs/vim), [Helix Mode](https://zed.dev/docs/helix).
