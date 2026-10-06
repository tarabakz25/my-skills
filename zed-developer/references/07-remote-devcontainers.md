# Remote development, WSL, and dev containers

## SSH architecture

Zed UI, Tree-sitter parsing/highlighting, unsaved state, and model UI remain local. Source files, terminals, tasks, language servers, and debugger sessions run on the remote host. Local extensions are propagated as needed for remote language tooling.

Before configuration, record local OS, remote OS/architecture, SSH command, internet/proxy restrictions, Zed version/channel, and whether the issue reproduces with plain `ssh`.

Open Remote Projects or use:

```text
zed ssh://[user@]host[:port]/absolute/path
zed ssh://[user@]host:~/project
```

Zed uses the `ssh` binary on `PATH` and `~/.ssh/config`, creates a ControlMaster per project, and multiplexes protocol/terminal/task connections. Prefer SSH keys/agent. Do not store passwords in Zed settings or URLs; command-line passwords leak through history/process listings.

## Settings placement

- Local user settings: UI concerns such as font/theme.
- Remote user settings: server concerns such as proxy and tool paths.
- `.zed/settings.json`: project behavior read in project context.
- Both local and remote sides can read project settings, but do not share each other's user settings.

When giving a setting, label exactly which machine/file gets it.

Restricted remote internet: `upload_binary_over_ssh: true` can have local Zed download/upload the matching server binary. Proxy settings/environment must be configured on the remote because it does not inherit the local proxy.

Remote host support and version requirements change. At the research baseline, macOS/Linux remote servers were supported; Windows could be a local client but was not a supported SSH remote server. Re-check current docs.

## Port forwarding

Use per-connection `port_forwards`. Default local binding should remain loopback. Binding `0.0.0.0` exposes the forwarded service to the network; warn explicitly and require user intent.

## WSL

Windows Zed can open WSL paths/workflows. Determine whether tools should execute in Windows or WSL. Do not mix Windows absolute paths, WSL paths, and environments. Verify `zed` CLI behavior from within the target distribution against current Windows docs.

## Dev containers

Prerequisites: `.devcontainer/devcontainer.json`, Docker or Podman on PATH. Podman requires current Zed setting (`use_podman` at baseline). BuildKit can be disabled with `dev_container_use_buildkit: false` for incompatible Docker-compatible engines.

Opening in a container builds if needed, launches, and reconnects. Tasks, terminals, and LSP execute inside. `customizations.zed.extensions` can specify extensions, but current feature maturity must be checked.

Changing `devcontainer.json` did not automatically rebuild at baseline. Stop the existing container safely and reopen; do not kill unrelated containers. Before issuing `docker kill`, identify the exact container and explain loss of running processes.

## Troubleshooting

1. Test plain SSH/container engine independently.
2. Check local Zed log and remote shell PATH/proxy.
3. Verify host architecture and free disk space.
4. Confirm project scope is not enormous; avoid opening `/` or huge home directories.
5. Check exact client/server version match and `~/.zed_server` state only after logs indicate it.
6. Preserve local unsaved buffers; reconnect rather than deleting remote state.
7. For container config changes, rebuild only the target container.

Official sources: [Remote Development](https://zed.dev/docs/remote-development), [Environment Variables](https://zed.dev/docs/environment), [Dev Containers](https://zed.dev/docs/dev-containers), [Windows](https://zed.dev/docs/windows).
