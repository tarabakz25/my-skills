# Developer workflows: Git, worktrees, debugger, REPL

## Git

Zed's Git Panel reflects working-tree/staging/branch changes, including command-line changes. Before suggesting a Git action, inspect repository state. Never discard, reset, force-push, or delete branches without explicit authorization and a recovery path.

Use repository-native hooks/config. Generated commit messages require review. Separate editor UI issues from Git state by checking `git status` in the same worktree.

## Linked worktrees and parallel work

Git worktrees isolate branches and are useful for parallel agents. Distinguish a Zed “worktree” (any opened root/file in its trust model) from a Git linked worktree.

- Create worktrees in the configured directory and avoid branch collisions.
- `.zed/tasks.json` hook `create_worktree` can initialize new worktrees; make it idempotent and never copy secrets by default.
- Confirm uncommitted changes before removing a linked worktree.
- Project trust is per host/path hierarchy and is not equivalent to Git trust.

## Debugger

Zed uses DAP. A working debug flow needs:

1. language/debug adapter installed,
2. project trust,
3. adapter executable available in the execution environment,
4. valid launch/attach scenario matching adapter schema,
5. source paths and build artifacts aligned, especially remote/container.

Start from the New Process Modal and current debugger docs. “Run” tasks are not automatically debuggable unless a DAP locator maps them. For attach, confirm target process and network exposure. Do not open debug ports publicly.

Debug diagnosis: inspect Debug Console and Zed log, verify adapter standalone, confirm launch vs attach, test minimal config, and check remote path mappings.

## REPL/Jupyter

Zed's REPL uses Jupyter kernels to run cells in editor files. Verify `jupyter`/kernel is installed in the selected toolchain/environment, not just another shell. Kernel discovery differs across local, remote, and container contexts. Avoid executing untrusted notebooks/code and review outputs containing secrets.

## Search, diagnostics, multibuffer

Teach workflows around actions:

- project/file/symbol search,
- go to definition/references,
- diagnostics navigation and quick fixes,
- multibuffer editing of search results/references,
- selections and multi-cursor.

Action names and shortcuts change with base keymap. Use Command Palette and All Actions for exact current binding.

Official sources: [Git](https://zed.dev/docs/git), [Debugger](https://zed.dev/docs/debugger), [REPL](https://zed.dev/docs/repl), [Diagnostics](https://zed.dev/docs/diagnostics), [Parallel Agents](https://zed.dev/docs/ai/parallel-agents).
