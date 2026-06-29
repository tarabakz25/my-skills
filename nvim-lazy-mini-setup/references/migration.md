# Migration checklist (packadd/mini.deps -> lazy.nvim)

Use this when the user already has a working config and wants to switch to lazy.nvim.

## 1) Confirm intent

- Do they want lazy.nvim as the only plugin manager?
- Are there any plugins installed via distro/package manager that should stay as-is?

## 2) Snapshot current behavior

- Note current plugin list and module list (mini.* and non-mini)
- Note essential keymaps and commands
- Note startup hooks (autocmds) and UI defaults

## 3) Add lazy.nvim bootstrap

- Add lazy.nvim bootstrap to `init.lua`.
- Ensure `vim.opt.rtp:prepend(lazypath)` happens before `require('lazy')`.

## 4) Translate plugins into lazy specs

- One file per feature/plugin under `lua/plugins/`.
- For mini.nvim modules:
  - Either keep `echasnovski/mini.nvim` and call module `setup()`.
  - Or depend on split repos like `echasnovski/mini.files` if you want finer-grained loading.

## 5) Remove old plugin-manager glue

Common things to delete/disable after verifying lazy is working:

- `packadd` for third-party plugins (except for temporary bootstrapping)
- `mini.deps` setup and any calls that register plugins through it
- custom `pack/*/start` plugin directories (optional; user decision)

## 6) Regenerate lockfile

- Start Neovim.
- Run `:Lazy sync`.
- Ensure `lazy-lock.json` is created/updated.

## 7) Verify

- Restart Neovim at least once.
- Run `:checkhealth`.
- Exercise the core workflows (file open, edit, git, lsp, format) the user cares about.
