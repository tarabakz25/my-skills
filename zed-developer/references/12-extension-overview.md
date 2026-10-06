# Zed extension architecture

## Capability selection

| Desired feature | Typical files | Rust/Wasm? |
|---|---|---|
| Grammar-only language | `extension.toml`, `languages/...`, Tree-sitter queries | No |
| Language server integration | above + `Cargo.toml`, `src/lib.rs` | Yes |
| Theme | `extension.toml`, `themes/*.json` | No |
| Icon theme | `extension.toml`, `icon_themes/*.json`, `icons/*.svg` | No |
| Snippets | `extension.toml`, `snippets/*.json` | No |
| Debug adapter/locator | manifest, schema, Rust | Yes |
| MCP server extension | manifest, Rust | Yes; check deprecation policy first |
| Extension slash commands | removed | Do not implement; use MCP where appropriate |
| ACP agent server extension | deprecated in favor of ACP Registry at baseline | Re-check registry approach |

Start with data-only. Add Rust only when a required API hook resolves/runs external tooling.

## Minimal manifest

```toml
id = "my-language"
name = "My Language"
version = "0.0.1"
schema_version = 1
authors = ["Name <email@example.com>"]
description = "Language support for My Language"
repository = "https://github.com/example/my-language"
```

The repository is a Git repository with `extension.toml` at the extension root. Required/optional capability tables vary; inspect current docs and maintained examples.

ID rules for publishing at the baseline:

- unique and immutable after publishing,
- ID/name must not include `zed`, `Zed`, or `extension`,
- descriptive suffixes such as `-theme` and `-snippets` are expected unless language/tool naming makes that redundant,
- check live `zed-industries/extensions/extensions.toml` before choosing.

## Rust/Wasm skeleton

```toml
[package]
name = "my-extension"
version = "0.0.1"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
zed_extension_api = "<latest-published-compatible-version>"
```

```rust
use zed_extension_api as zed;

struct MyExtension;

impl zed::Extension for MyExtension {
    fn new() -> Self { Self }
}

zed::register_extension!(MyExtension);
```

Do not copy the `0.1.0` API version from the generic docs example. At the research baseline crates.io published `0.7.0`, while Zed `main` declared unpublished `0.8.0`; query crates.io and compatibility docs at implementation time.

Wasm caveats: `cfg` and `std::env::var` do not behave as native code authors may expect. Use `current_platform`, Worktree/Project APIs, and Zed-provided process/download/npm APIs.

## Extension capabilities

Least-privilege capabilities are governed by manifest/user settings. Current kinds include:

- `process:exec` with command and argument patterns,
- `download_file` with host/path restrictions,
- `npm:install` with package restriction.

Users can narrow `granted_extension_capabilities`. An extension must handle denied capability errors clearly. Avoid wildcard grants when exact hosts/commands/packages suffice.

## External executable lifecycle

- Do not bundle language/debug/MCP servers in the extension.
- Prefer an existing executable on the user's PATH when policy/design supports it.
- Otherwise resolve latest supported release, download through Zed API, verify archive/layout as possible, cache in extension work directory, and avoid checking updates on every session.
- Support platform/architecture explicitly and return actionable errors.
- Never alter shell profiles or global environment silently.

## Local development

Install Rust via rustup (non-rustup installs can break dev-extension build). In Extension Gallery choose Install Dev Extension and select the extension root. A published copy is overridden/uninstalled while the dev extension is active. Use `zed: open log`; start `zed --foreground` for Rust `println!`/`dbg!` output.

Official sources: [Developing Extensions](https://zed.dev/docs/extensions/developing-extensions), [Capabilities](https://zed.dev/docs/extensions/capabilities), [Installing Extensions](https://zed.dev/docs/extensions/installing-extensions), [Extension API](https://docs.rs/zed_extension_api).
