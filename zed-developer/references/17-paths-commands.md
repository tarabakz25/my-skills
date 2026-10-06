# Paths and commands quick reference

Always prefer the command palette to locate files because XDG/channel/platform behavior can vary.

| Item | macOS | Linux | Windows |
|---|---|---|---|
| User settings | `~/.config/zed/settings.json` | `${XDG_CONFIG_HOME:-~/.config}/zed/settings.json` | `%APPDATA%\Zed\settings.json` |
| Keymap | `~/.config/zed/keymap.json` | `${XDG_CONFIG_HOME:-~/.config}/zed/keymap.json` | `%APPDATA%\Zed\keymap.json` |
| Global tasks | `~/.config/zed/tasks.json` | `${XDG_CONFIG_HOME:-~/.config}/zed/tasks.json` | `%APPDATA%\Zed\tasks.json` |
| Snippets folder | `~/.config/zed/snippets` | `${XDG_CONFIG_HOME:-~/.config}/zed/snippets` | `%APPDATA%\Zed\snippets` (verify current docs/UI) |
| Local themes | `~/.config/zed/themes` | `${XDG_CONFIG_HOME:-~/.config}/zed/themes` | `%APPDATA%\Zed\themes` |
| Extensions | `~/Library/Application Support/Zed/extensions` | `${XDG_DATA_HOME:-~/.local/share}/zed/extensions` | `%LOCALAPPDATA%\Zed\extensions` |
| Logs | `~/Library/Logs/Zed/Zed.log` | `${XDG_DATA_HOME:-~/.local/share}/zed/logs/Zed.log` | `%LOCALAPPDATA%\Zed\logs\Zed.log` |
| Workspace DB | `~/Library/Application Support/Zed/db` | `${XDG_DATA_HOME:-~/.local/share}/zed/db` | `%LOCALAPPDATA%\Zed\db` |
| Personal Agent instructions | `~/.config/zed/AGENTS.md` | `${XDG_CONFIG_HOME:-~/.config}/zed/AGENTS.md` | `%APPDATA%\Zed\AGENTS.md` |
| Zed Agent skills | `~/.agents/skills/` | `~/.agents/skills/` | `~\.agents\skills\` |

Project files:

- `.zed/settings.json`
- `.zed/tasks.json`
- `.devcontainer/devcontainer.json`
- `.editorconfig`
- `.agents/skills/<skill>/SKILL.md` (Zed Agent)

Useful commands/actions (search exact label in current Command Palette):

- `zed: open settings`, `zed: open settings file`, `zed: open project settings`, `zed: open default settings`
- `zed: open keymap file`
- `dev: open key context view`
- `zed: open tasks`, `zed: open project tasks`, `task: spawn`, `task: rerun`
- `snippets: open folder`
- `zed: extensions`, `zed: install dev extension`
- `zed: open log`, `zed: reveal log in file manager`
- `zed: about`, copy system specs, copy installed extensions
- `editor: restart language server`
- `toolchain: select`
- `workspace::ToggleWorktreeSecurity`, `workspace::ClearTrustedWorktrees`
- `agent: open skill creator`, `agent: create skill from url`
- `dev: open acp logs`

Action labels shown in UI and internal action identifiers are not interchangeable. Verify before writing keymap JSON.
