---
name: zed-developer
description: Comprehensive Zed editor expertise for configuring settings, appearance, keybindings, languages, LSP/formatters, tasks, terminals, remote development, AI/collaboration, troubleshooting, and developing/testing/publishing Zed extensions. Use whenever a user asks how to use, customize, diagnose, automate, or extend Zed.
---
# Zed Developer

Use this skill as the routing layer for any Zed editor task. Load only the references needed for the current request.

## Non-negotiable operating rules

1. Prefer current primary sources: Zed docs, Zed source, `zed-industries/extensions`, `zed_extension_api`, and the schemas linked from those sources.
2. Treat keys, actions, schemas, API versions, paths, feature status, and marketplace policy as version-sensitive. Never invent or rely on memory when verification is possible.
3. Before editing, inspect the existing file and identify OS, Zed channel/version, scope (user/project/remote), and desired behavior when these affect correctness.
4. Make the smallest valid change. Preserve unrelated settings, comments, formatting, and user intent. Do not replace a whole settings file just to add one key.
5. Show the exact target path and explain whether the change is global, project-local, remote-server-side, or container-side.
6. Validate generated JSON/JSONC/TOML/Rust when tools are available. Never claim Zed accepted a change unless it was actually tested in Zed.
7. Back up or produce a patch before risky recovery. Never delete databases/configuration as a first troubleshooting step.
8. Do not expose secrets. Do not put API keys/passwords in `settings.json`, project files, logs, examples, or extension repositories.
9. Distinguish verified fact from inference. If current docs and checked source differ, state the mismatch and prefer released behavior for the user's installed Zed version.
10. For destructive commands, publishing, or external changes, request explicit approval first.

## Route the request

| User intent | Load first | Often also load |
|---|---|---|
| Install, update, CLI, migration, basic usage | `references/01-installation-cli-usage.md` | `references/10-workflows.md` |
| Edit `settings.json`, project settings, profiles/channels | `references/02-settings.md` | `references/03-appearance.md`, `references/05-languages-lsp-formatting.md` |
| Themes, icons, fonts, visual layout | `references/03-appearance.md` | `references/13-extension-data-only.md` |
| Shortcuts, contexts, Vim/Helix/base keymaps | `references/04-keybindings.md` | `references/18-recipes.md` |
| Language support, LSP, formatter, lint, semantic tokens | `references/05-languages-lsp-formatting.md` | `references/12-extension-language.md` |
| Tasks, terminal, environment variables, snippets | `references/06-tasks-terminal-env-snippets.md` | `references/18-recipes.md` |
| SSH, WSL, dev containers | `references/07-remote-devcontainers.md` | `references/16-security-privacy.md` |
| Agent Panel, Skills, Instructions, MCP, external agents | `references/08-ai.md` | `references/16-security-privacy.md` |
| Collaboration, channels, calls | `references/09-collaboration.md` | `references/16-security-privacy.md` |
| Git, worktrees, debugger, REPL, daily workflows | `references/10-workflows.md` | `references/06-tasks-terminal-env-snippets.md` |
| Broken startup, LSP, extension, GPU, config, performance | `references/11-troubleshooting.md` | affected feature reference |
| Start or design a Zed extension | `references/12-extension-overview.md` | capability-specific reference |
| Language/grammar/LSP extension | `references/12-extension-language.md` | `references/15-extension-testing-publishing.md` |
| Theme/icon/snippet extension | `references/13-extension-data-only.md` | `references/15-extension-testing-publishing.md` |
| Debug adapter or MCP extension | `references/14-extension-dap-mcp.md` | `references/15-extension-testing-publishing.md` |
| Publish/update extension | `references/15-extension-testing-publishing.md` | capability-specific reference |
| Security, worktree trust, privacy, extension capabilities | `references/16-security-privacy.md` | relevant feature reference |
| Exact paths/commands/action names | `references/17-paths-commands.md` | `references/00-source-policy.md` |
| Ready-made configuration patterns | `references/18-recipes.md` | relevant feature reference |

## Standard workflow: configuration changes

1. Read `references/02-settings.md` and the feature-specific reference.
2. Determine target scope and path. For remote work, separate local UI settings, remote server settings, and project settings.
3. Read the current file. If absent, create only the minimum object/array required.
4. Confirm the key and value shape against current docs, Settings Editor, default settings, or schema.
5. Patch without dropping comments or sibling keys. Remember: objects usually merge across settings layers, but some arrays replace defaults.
6. Validate syntax with `scripts/validate_jsonc.py <file>` when possible.
7. Explain reload/restart needs and a rollback step.

## Standard workflow: appearance changes

1. Separate theme selection, theme override, font choice, UI density, and icon theme; do not solve all with a monolithic theme.
2. Prefer `theme_overrides` for a small adjustment; use a local/theme extension only when creating a distributable complete theme.
3. Verify the font is installed and use exact family names. Keep terminal, buffer, and UI fonts distinct unless requested otherwise.
4. Provide both light and dark values when using system mode.
5. Validate contrast and preserve a copy of the previous selection.

## Standard workflow: extension development

1. Read `references/12-extension-overview.md`, then the capability-specific reference and `references/15-extension-testing-publishing.md`.
2. Choose the smallest capability set. Data-only themes/icons/snippets and grammar-only language support should not gain Rust code unnecessarily.
3. Check the live registry for ID collisions before committing to an ID. An ID is immutable after publishing.
4. Use the latest **published compatible** `zed_extension_api`; do not copy the stale version in an illustrative docs snippet. Verify crates.io and the compatibility table.
5. Declare least-privilege extension capabilities. Do not bundle language/debug/MCP servers; resolve or download them through approved APIs.
6. Install as a dev extension, inspect logs, run Zed foreground for Rust output, and test success/failure paths on intended platforms.
7. Validate manifest, schemas, license, version parity, HTTPS submodule URL, branch-attached commit, and registry sorting before a publishing PR.

## Standard workflow: troubleshooting

1. Ask for symptom, reproduction, OS, Zed version/channel, local vs remote/container, and recent changes—but do not re-ask facts already supplied.
2. Start with the least invasive isolation: diagnostics/log, syntax validation, restart affected LSP, disable one suspect extension, compare a minimal project.
3. Gather `zed: about`, copied system specs, installed extension versions, and relevant recent log lines. Redact secrets and private paths before sharing.
4. Change one variable at a time and record expected evidence.
5. Only after backup, move (never immediately delete) the channel-specific workspace database to test corruption.
6. Give rollback instructions and distinguish a workaround from a root-cause fix.

## Bundled resources

- `references/`: detailed, task-specific knowledge and official source map.
- `assets/templates/`: conservative starting points; placeholders must be replaced before use.
- `scripts/validate_jsonc.py`: syntax-check JSON/JSONC without modifying it.
- `scripts/validate_extension.py`: inspect a Zed extension manifest/layout and common publishing mistakes.
- `scripts/check_skill.py`: validate this Cursor skill package and internal links.
- `scripts/check_sources.py`: optionally check official source URLs for redirects/failures.

## Freshness rule

The package baseline is recorded in `references/00-source-policy.md`. For a question involving version-sensitive behavior, verify current official documentation before asserting exact behavior. If offline, state the baseline date and mark anything likely to have changed.
