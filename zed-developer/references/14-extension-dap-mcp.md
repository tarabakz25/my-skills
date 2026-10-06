# Debug adapter and MCP extensions

## Debug adapters (DAP)

Manifest:

```toml
[debug_adapters.example-dap]
schema_path = "debug_adapter_schemas/example-dap.json"

[debug_locators.example-locator]
```

`schema_path` may default to `debug_adapter_schemas/<adapter-id>.json`, but a schema is mandatory. Define launch/attach configuration accurately; schema is user-facing contract.

Required/current APIs include:

- `get_dap_binary`: resolve adapter command/args/env; honor user-provided path.
- `dap_request_kind`: determine launch versus attach; do not perform expensive setup here.
- `dap_config_to_scenario`: strongly recommended to map generic UI configuration.
- locator `dap_locator_create_scenario`: fast filter/mapping from tasks.
- optional second phase `run_dap_locator`: resolve artifacts after successful build.

Do not download-check every debug session; cache and check periodically. Test launch, attach, user path, missing executable, build failure, cancellation, remote/container path mapping, and all schema branches. Locators receive unlikely tasks; return `None` quickly.

## MCP extension status

At the 2026-07-15 baseline, Zed planned to deprecate MCP server extensions in favor of the official MCP Registry. Before implementing, check:

- current Zed MCP docs,
- official MCP registry publishing,
- Zed tracking issue/policy,
- whether a custom local/remote server can be added directly in UI instead.

Legacy/current extension manifest shape:

```toml
[context_servers.example]
```

Implement `context_server_command` returning executable/args/env and optionally configuration UI through current API. This model was intended for binary or npm-published servers; remote servers should be configured natively.

Security:

- least-privilege `process:exec`, `download_file`, or `npm:install`,
- never log tokens or embed credentials,
- explain network/data destinations,
- validate server package/source/version,
- handle offline and denied permission,
- do not modify shell environment globally.

## Removed/deprecated mechanisms

Extension-provided slash commands have been removed; use MCP tools/context where appropriate. ACP agent-server extensions were deprecated in favor of the ACP Registry at the baseline. Do not resurrect obsolete APIs from old examples.

Official sources: [Debugger Extensions](https://zed.dev/docs/extensions/debugger-extensions), [MCP Extensions](https://zed.dev/docs/extensions/mcp-extensions), [MCP](https://zed.dev/docs/ai/mcp), [ACP Registry](https://agentclientprotocol.com/registry).
