# Appearance

## Choose the least complex mechanism

1. Select an installed theme/icon theme for preference changes.
2. Use font/layout settings for typography and density.
3. Use `theme_overrides` for a few colors or syntax styles.
4. Use a local theme JSON for a complete private theme.
5. Build a separate theme/icon-theme extension only for distribution.

## Theme and icon selection

```jsonc
{
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "One Dark"
  },
  "icon_theme": {
    "mode": "system",
    "light": "Zed (Default)",
    "dark": "Zed (Default)"
  }
}
```

Commands include the Theme Selector (`ctrl-k ctrl-t` in the documented default), light/dark toggle, and `icon theme selector: toggle`. Search the Command Palette if user keymaps differ.

A static string theme is valid, but switching modes can convert it to the dynamic object. Set both `light` and `dark` explicitly after conversion.

## Fonts

- `buffer_font_family`, `buffer_font_size`, `buffer_font_weight`, `buffer_font_features`, `buffer_font_fallbacks`, `buffer_line_height`: editor text.
- `ui_font_family`, `ui_font_size`: interface.
- `terminal.font_family`, `terminal.font_size`: integrated terminal.
- `.ZedMono` refers to Zed's bundled editor font.
- Font family must match an installed font's exact family name. A font file sitting in a repository is not automatically installed.
- Disable common ligatures with `"buffer_font_features": { "calt": false }`.
- `buffer_line_height` accepts documented presets or a custom object; verify current accepted shape.

```jsonc
{
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "buffer_font_features": { "calt": false },
  "buffer_line_height": "standard",
  "ui_font_family": "Inter",
  "ui_font_size": 16,
  "terminal": {
    "font_family": "JetBrains Mono",
    "font_size": 14
  }
}
```

## Targeted theme overrides

```jsonc
{
  "theme_overrides": {
    "One Dark": {
      "editor.background": "#202124",
      "syntax": {
        "comment": { "font_style": "italic" },
        "comment.doc": { "font_style": "italic" }
      }
    }
  }
}
```

Override the exact active theme name. If light and dark themes differ, provide overrides for both or explain that only one side changes. Check contrast for selection, diagnostics, diff colors, inactive text, and terminal ANSI colors—not only editor background.

## Local themes

- macOS/Linux: `~/.config/zed/themes/`
- Windows: `%APPDATA%\Zed\themes\` (equivalent documented user configuration area)

Use Zed Theme Builder for full-theme authoring and export. Include the current theme schema URL in JSON. Theme family requires `name`, `author`, and `themes`; each theme requires `name`, `appearance`, and `style` under schema v0.2.0 at research baseline.

## Common failures

- Wrong theme display name: inspect Theme Selector rather than extension ID.
- Font silently falls back: verify installation and family name; add deliberate fallbacks.
- Override appears only in dark mode: add matching active light-theme key.
- Syntax color does nothing: Tree-sitter capture or semantic token may differ. Inspect language highlighting and semantic-token mode.
- UI too dense/large after editor font change: buffer and UI font sizes are independent.
- Complete custom theme mixed into a language extension: marketplace guidance asks themes/icon themes to be separate extensions.

Official sources: [Appearance](https://zed.dev/docs/appearance), [Themes](https://zed.dev/docs/themes), [Icon Themes](https://zed.dev/docs/icon-themes), [Theme Extensions](https://zed.dev/docs/extensions/themes), [Icon Theme Extensions](https://zed.dev/docs/extensions/icon-themes).
