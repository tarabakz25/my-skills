# mini.nvim module recipes

This is a grab-bag; pick only what the user asked for.

## Common modules

- `mini.basics`: sensible defaults; can replace a lot of manual `vim.opt`.
- `mini.files`: file explorer.
- `mini.surround`: surround motions.
- `mini.comment`: commenting.
- `mini.pairs`: autopairs.
- `mini.statusline` / `mini.tabline`: lightweight UI.
- `mini.starter`: start screen.
- `mini.pick`: picker (can replace Telescope for some users).
- `mini.indentscope`: indent guides and scope textobject.

## Suggested defaults

### mini.basics

If the config already has extensive option tuning, avoid enabling `mini.basics` wholesale.

```lua
require('mini.basics').setup({
  options = {
    basic = true,
    extra_ui = true,
    win_borders = 'single',
  },
  mappings = {
    basic = false, -- avoid surprising keymaps
  },
  autocommands = {
    basic = true,
  },
})
```

### mini.files

Minimal:

```lua
require('mini.files').setup()
```

Typical keymaps:

- `<leader>e`: open explorer at current file
- `<leader>E`: open explorer at cwd

### mini.surround

```lua
require('mini.surround').setup()
```

If the user has muscle memory from other surround plugins, ask before changing mappings.

### mini.comment

```lua
require('mini.comment').setup()
```

### mini.statusline

```lua
require('mini.statusline').setup()
```

If they use another statusline plugin, skip this.

### mini.starter

```lua
require('mini.starter').setup()
```

### mini.pick

```lua
require('mini.pick').setup()
```

`mini.pick` is useful for users who want to keep dependencies small.
