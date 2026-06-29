# Templates (lazy.nvim + mini.nvim)

Keep these as starting points; adapt to the repo's existing structure.

## Minimal init.lua (lazy.nvim bootstrap + modular loading)

```lua
-- init.lua

vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

-- lazy.nvim bootstrap
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
local uv = vim.uv or vim.loop
if not uv.fs_stat(lazypath) then
  vim.fn.system({
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable',
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require('options')
require('keymap')

require('lazy').setup({
  spec = {
    { import = 'plugins' },
  },
  -- Keep this conservative; users can tune later.
  defaults = { lazy = true },
  install = { colorscheme = { 'habamax' } },
  checker = { enabled = false },
})
```

## options.lua + keymap.lua entrypoints

```lua
-- lua/options/init.lua
require('options.basic')
require('options.ui')
```

```lua
-- lua/keymap.lua
-- Keep global keymaps here. Plugin-specific keymaps live with the plugin.
```

## plugins/init.lua aggregator

```lua
-- lua/plugins/init.lua
return {
  require('plugins.mini'),
  -- require('plugins.treesitter'),
  -- require('plugins.lsp'),
}
```

If you prefer the import style:

```lua
-- lua/plugins/init.lua
return {}
```

And then in `lazy.setup`: `{ import = 'plugins' }`.

## mini.nvim via lazy.nvim (single module)

```lua
-- lua/plugins/mini.lua
return {
  'echasnovski/mini.nvim',
  version = false,
  config = function()
    require('mini.basics').setup({
      options = { basic = true, extra_ui = true, win_borders = 'single' },
      mappings = { basic = false },
      autocommands = { basic = true },
    })

    require('mini.pairs').setup()
    require('mini.comment').setup()
    require('mini.surround').setup()

    require('mini.statusline').setup()
    require('mini.tabline').setup()

    require('mini.files').setup()
  end,
}
```

## mini.files keymap example

```lua
-- Example: lua/plugins/mini_files.lua
return {
  'echasnovski/mini.files',
  version = false,
  keys = {
    {
      '<leader>e',
      function()
        require('mini.files').open(vim.api.nvim_buf_get_name(0), true)
      end,
      desc = 'File explorer (mini.files)',
    },
  },
  config = function()
    require('mini.files').setup()
  end,
}
```
