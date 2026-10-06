# Source policy and freshness

## Baseline

- Research date: **2026-07-15**.
- Zed source inspected at commit `6b9f448ffc1d0807c57dfc94e76b1b4c4a319e7a`.
- Official extension registry inspected at commit `19e67d9debea2d6a1c7a54923ca62f9e5143fd10`.
- Cursor packaging follows the current official Agent Skills documentation.
- The latest published `zed_extension_api` observed during research was `0.7.0`; Zed `main` declared an unpublished `0.8.0`. This is precisely why generated extension code must query the latest **published and compatible** version instead of hardcoding either number.

## Authority order

Use sources in this order when claims conflict:

1. Behavior in the user's installed Zed version and its built-in default settings/action list.
2. Current released Zed documentation.
3. Tagged/released Zed source matching the user's version.
4. Current official extension registry and representative maintained extension repositories.
5. `zed_extension_api` docs and compatibility table for the chosen published crate version.
6. Zed `main` branch for upcoming behavior, explicitly labeled unreleased.
7. Community sources only when official sources are silent, clearly attributed.

## Primary sources

- Zed docs: <https://zed.dev/docs/>
- All settings: <https://zed.dev/docs/reference/all-settings>
- All actions: <https://zed.dev/docs/all-actions>
- Zed source: <https://github.com/zed-industries/zed>
- Extension registry: <https://github.com/zed-industries/extensions>
- Extension API crate: <https://crates.io/crates/zed_extension_api>
- Extension API docs: <https://docs.rs/zed_extension_api>
- Theme schema: <https://zed.dev/schema/themes/v0.2.0.json>
- Icon theme schema: <https://zed.dev/schema/icon_themes/v0.3.0.json>
- Agent Skills in Cursor: <https://cursor.com/docs/skills>

## Verification rules

- Settings keys: check All Settings, Settings Editor, or `zed: open default settings`.
- Actions: check All Actions, default keybindings, or search the Command Palette; action identifiers are case-sensitive.
- Extension API: check crates.io, docs.rs, and compatible Zed versions. Do not infer APIs from `main` unless targeting Nightly/dev.
- Theme/icon schema: use the `$schema` URL present in the generated JSON and validate against it.
- Marketplace state: search the live registry for collisions and review current policy before publishing.
- Feature status: preserve labels such as beta, experimental, deprecated, or removed.

## Known fast-moving areas

AI provider behavior, ACP/MCP registries, tool permissions, Windows support, dev containers, debugger APIs, extension capabilities, and extension API versions are especially likely to change. Re-verify them for any implementation request.
