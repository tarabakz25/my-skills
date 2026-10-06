# Troubleshooting and recovery

## Triage record

Capture:

- exact symptom and expected behavior,
- minimal reproduction,
- Zed version/channel (`zed: about` or `zed --version`),
- OS/architecture/system specs,
- local/SSH/WSL/container,
- installed extension names/versions,
- project trust state,
- recent config/extension/toolchain changes,
- relevant logs with secrets redacted.

Commands: `zed: copy system specs into clipboard`, `zed: copy installed extensions into clipboard`, `zed: open log`, `zed: reveal log in file manager`.

## Logs

- macOS: `~/Library/Logs/Zed/Zed.log`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/zed/logs/Zed.log`
- Windows: `%LOCALAPPDATA%\Zed\logs\Zed.log`

`zed: open log` shows recent lines. `zed --foreground` provides useful extension stdout/stderr and INFO logs. Do not paste full logs blindly; remove API keys, tokens, usernames, private paths/code, remote hostnames, and prompt contents.

## Isolation ladder

1. Validate the edited JSONC/TOML/schema.
2. Reproduce in a minimal file/project.
3. Restart only the affected language server (`editor: restart language server`) or reconnect remote.
4. Temporarily revert the last setting change.
5. Disable one suspect extension, not all state.
6. Compare CLI vs GUI launch environment and local vs remote/container.
7. Use an isolated user data directory if appropriate.
8. Check platform GPU/backend guidance for startup/render problems.
9. Profile a reproducible performance issue with the platform-recommended profiler.
10. Only then test workspace database regeneration.

## Workspace database recovery

Locations:

- macOS: `~/Library/Application Support/Zed/db`
- Linux/FreeBSD: `${XDG_DATA_HOME:-~/.local/share}/zed/db`
- Windows: `%LOCALAPPDATA%\Zed\db`

Channel database names include `0-stable`, `0-preview`, `0-nightly`, and `0-dev` at baseline.

Safe protocol:

1. Quit Zed and verify no process remains.
2. Back up/move only the affected channel database, with timestamp.
3. Relaunch and test.
4. Understand this resets recent projects/open tabs/session state.
5. If it does not help, quit, restore the backup, and continue diagnosis.

Never delete the entire data/config directory as the first step.

## Symptom matrix

| Symptom | First checks |
|---|---|
| Settings ignored | target scope/path, JSONC syntax, project trust, nested/project/channel override, user-only key |
| Shortcut ignored | exact action, active context view, later/more-specific binding, modal mode, chord prefix |
| LSP absent | recognized language, trust, server order/disable list, PATH/env, logs |
| Formatter absent/wrong | per-language override, formatter stdin behavior, server capability, save setting |
| Extension won't build | rustup toolchain, published compatible API, manifest/capabilities, foreground logs |
| SSH fails | plain SSH, agent/key prompt, ssh binary/config, proxy/internet, server architecture/version |
| Container stale | target container identity, config changed, rebuild/reopen requirement |
| Slow indexing | huge root, inclusion/exclusion replacement, symlinks, language server CPU |
| Rendering/startup issue | platform docs, log GPU/Vulkan errors, driver/backend, isolated data |

## Bug report quality

Include deterministic steps, smallest sample repository if shareable, before/after versions, system specs, extension list, concise redacted log excerpt, and performance trace/crash dump when requested. State what isolation steps changed the outcome.

Official sources: [Troubleshooting](https://zed.dev/docs/troubleshooting), [Linux](https://zed.dev/docs/linux), [Windows](https://zed.dev/docs/windows), [Debugging Crashes](https://zed.dev/docs/development/debugging-crashes).
