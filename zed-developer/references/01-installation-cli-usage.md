# Installation, CLI, migration, and core usage

## Platform check

Confirm OS, CPU architecture, installation channel (Stable/Preview/Nightly), and whether the user wants local, WSL, SSH, or container operation. Prefer the official installer/package instructions for the target platform because package names and requirements change.

- Official installation: <https://zed.dev/docs/installation>
- Platform notes: [macOS](https://zed.dev/docs/macos), [Linux](https://zed.dev/docs/linux), [Windows](https://zed.dev/docs/windows)
- Release channels can coexist. Keep channel-specific data/log/database paths distinct when diagnosing.

## CLI

Syntax: `zed [OPTIONS] [PATHS]...`. Linux package binaries may be named `zed` or `zeditor`; do not assume one. On macOS, install the CLI through `cli: install cli binary`. On Windows, use bundled `zed.exe` and ensure the install directory is on `PATH`.

Common patterns:

```bash
zed .                        # open current directory
zed file.rs:42:10            # line and column
zed file1 file2              # multiple paths
zed --diff old.rs new.rs     # diff
zed -n project               # new workspace
zed -a file                  # add to focused workspace
zed -r project               # replace/reuse workspace
cat output.txt | zed -       # stdin via temporary file
zed --wait file              # block until file closes
zed --foreground .           # attached logs/stdout
zed --version
```

`--wait` is suitable for `$EDITOR`/Git and reports whether files were saved. `--user-data-dir` creates an isolated data directory, useful for diagnosis; do not confuse this with the config directory.

Supported URL families include `zed://`, `file://`, and `ssh://`. For exact current options, run `zed --help` on the user's installation.

## Navigation mental model

Teach actions rather than fixed shortcuts when portability matters:

- Command Palette: discover actions and current bindings.
- Project Panel: files/worktrees.
- Outline/symbol search: structure navigation.
- Multibuffers: search results, diagnostics, and references can be edited as one surface.
- Git Panel: working tree, staging, commits.
- Tasks/Terminal: repeatable project commands versus interactive shell.
- Agent Panel/Inline Assistant: native AI surfaces.
- Remote Projects: SSH/WSL/dev containers.

Shortcuts vary by OS and base keymap. State an action name plus the documented/default shortcut, and ask the user to check the Command Palette if customized.

## Migration

For VS Code/JetBrains/WebStorm/IntelliJ migrations:

1. Inventory only behavior the user values: keymap, formatter, LSP, tasks, snippets, theme, terminal, remote, and extensions.
2. Select the closest base keymap; do not transliterate every shortcut prematurely.
3. Map settings semantically, not key-for-key. Zed is not VS Code and does not accept arbitrary VS Code settings/extensions.
4. Move repository-wide conventions to `.editorconfig` and tool-native files where possible.
5. Rebuild automation as `.zed/tasks.json` or import only supported VS Code task semantics.
6. Install Zed-native extensions; verify capabilities rather than name similarity.
7. Test format, lint, run, debug, and remote workflows before deleting old editor configuration.

## Uninstall and recovery

Use official uninstall guidance. Before removing application data, distinguish:

- configuration (`settings.json`, `keymap.json`, tasks, snippets, themes),
- data (extensions, language servers, workspace database),
- logs,
- the application binary.

Never delete all of them when the request is only to reinstall the app. Back up user-authored configuration first.
