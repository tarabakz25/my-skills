# Data-only extensions: themes, icon themes, snippets

## Theme extensions

Layout: `extension.toml` plus `themes/*.json`. Use the schema declared by current docs; baseline: `https://zed.dev/schema/themes/v0.2.0.json`.

```json
{
  "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
  "name": "Example Theme Family",
  "author": "Example Author",
  "themes": [
    {
      "name": "Example Dark",
      "appearance": "dark",
      "style": {
        "editor.background": "#1e1e1e",
        "editor.foreground": "#d4d4d4",
        "syntax": {
          "comment": { "color": "#6a9955", "font_style": "italic" }
        }
      }
    }
  ]
}
```

Theme family requires `name`, `author`, `themes`; each theme requires `name`, `appearance`, `style` at baseline. Use Theme Builder and test every UI state: focus, hover, selection, diagnostics, git diff, search, tabs, panels, collaborators, terminal ANSI, and light/dark contrast.

## Icon theme extensions

Layout:

```text
extension.toml
icon_themes/example.json
icons/*.svg
```

Baseline schema: `https://zed.dev/schema/icon_themes/v0.3.0.json`. Paths resolve from extension root. Define collapsed/expanded directory and chevron icons, named directories, `file_stems`, `file_suffixes`, and `file_icons`, including `default` fallback.

SVGs must be minimal, safe, and license-compatible. Test case sensitivity and filenames with multiple dots. Do not assume suffix mapping accepts a leading dot.

## Snippet extensions

Register relative paths in manifest:

```toml
snippets = ["./snippets/rust.json", "./snippets/snippets.json"]
```

Filename is lowercase language display name; `snippets.json` is global. Content follows the same snippet JSON format as user snippets. Test trigger uniqueness, placeholders, multiline indentation, and literal dollar escaping.

## Packaging policy

At the baseline, themes and icon themes should be published as distinct extensions rather than bundled with language/other features, even if source lives in one repository. Keep only required assets. Use naming suffix conventions and accepted license.

## Validation

- JSON syntax and `$schema`.
- All referenced icons/files exist with exact case.
- No absolute/local paths.
- Theme/icon display names unique within family.
- Dark/light appearance correct.
- Manifest version and registry version match.
- License covers copied palettes/icons/snippets as well as original code/assets.

Official sources: [Theme Extensions](https://zed.dev/docs/extensions/themes), [Icon Theme Extensions](https://zed.dev/docs/extensions/icon-themes), [Snippet Extensions](https://zed.dev/docs/extensions/snippets), [Theme Builder](https://zed.dev/theme-builder).
