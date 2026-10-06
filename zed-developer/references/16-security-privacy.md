# Security, trust, capabilities, and privacy

## Worktree trust

New roots begin in Restricted Mode until trusted. Restricted Mode blocks parsing/applying `.zed/settings.json` and installing/spawning project language or MCP servers. Global tools can still run independently.

Trust via title-bar warning/security modal or `workspace::ToggleWorktreeSecurity`. Trust persists for manual grants. `workspace::ClearTrustedWorktrees` clears decisions and restarts Zed so untrusted project tooling does not persist. Parent-directory trust covers descendants; grant it only deliberately.

Avoid recommending:

```json
{ "session": { "trust_all_worktrees": true } }
```

unless the user understands this bypass. It expands supply-chain exposure from project settings/tool downloads.

## Extension capabilities

Users control `granted_extension_capabilities`. Current categories include command execution, file download host/path, and npm package install. Extension authors should request exact command/host/package. Users should not globally wildcard privileges solely to silence an error; identify which extension needs what and why.

## Secrets

- Provider keys entered through Zed are stored in system keychain rather than `settings.json` according to current docs.
- Never commit secrets to `.zed/settings.json`, tasks, snippets, devcontainer, instructions, skill resources, or extension manifests.
- Environment variables reduce accidental commits but remain visible to child processes/tools; scope and redact them.
- Logs, ACP logs, prompts, task output, crash dumps, and profiler traces can contain code/paths/tokens. Review before sharing.
- SSH passwords must not go into persisted connection settings or command history; use keys/agent.

## AI privacy boundaries

Distinguish:

- Zed-hosted models and Zed/provider agreements,
- user's provider API key/subscription and provider terms,
- gateways/upstreams,
- local model server,
- external agent and its provider,
- terminal CLI/TUI,
- MCP servers/external services,
- edit prediction provider.

At the baseline, Zed stated it did not retain prompts/code context by default, while hosted providers had no-training/zero-retention agreements except provider-designated safety-retention models. Terms and model exceptions can change; verify current privacy page and provider terms. Edit Prediction can send local editing context per keystroke. External agents, terminal tools, MCP servers, and gateways have independent boundaries.

## Safe recommendations

1. Minimize context and tools.
2. Keep trust/confirm prompts for write, execute, network, and external-system actions.
3. Review project instructions and skills from cloned repositories.
4. Use non-production data in debugging.
5. Separate personal and company provider accounts/configuration.
6. Check organization admin/privacy policy before enabling AI/collaboration.
7. Explain what leaves the machine and to which service.

Official sources: [Worktree Trust](https://zed.dev/docs/worktree-trust), [Extension Capabilities](https://zed.dev/docs/extensions/capabilities), [AI Privacy](https://zed.dev/docs/ai/privacy-and-security), [Telemetry](https://zed.dev/docs/telemetry), [Privacy for Business](https://zed.dev/docs/business/privacy).
