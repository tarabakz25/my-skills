---
name: nvim-lazy-mini-setup
description: Help bootstrap, migrate, and maintain a modular Neovim configuration using lazy.nvim (plugin manager) and mini.nvim (core UX modules). Use when asked to set up or refactor Neovim config structure (init.lua, lua/options, lua/plugins), add or configure mini.* modules (mini.files, mini.surround, mini.comment, mini.statusline, mini.starter, etc), convert an existing setup (e.g. packadd/mini.deps) to lazy.nvim, troubleshoot lazy.nvim bootstrapping/lockfile issues, or standardize keymaps/docs around a lazy.nvim + mini.nvim stack.
---

# Nvim Lazy Mini Setup

## Workflow

### 1) Ask For Requirements (keep it short)

Ask only what you need to choose the right baseline:

- Target OS (macOS/Linux/Windows) and Neovim version constraints
- New config vs migrate an existing config (and where it lives)
- Plugin manager choice: lazy.nvim only (recommended) vs keep existing (e.g. mini.deps)
- mini.nvim modules they want (files, surround, comment, statusline, starter, pairs, indentscope, pick, etc)
- Opinionated choices: completion (nvim-cmp vs native), LSP (mason+lspconfig?), formatting (conform?), linting (nvim-lint?)

If the user doesn't care, default to a minimal, fast baseline: lazy.nvim + mini.nvim + built-in LSP, and leave completion optional.

### 2) Inspect The Current State

- If in a repo/worktree: list files and identify current entrypoint(s): init.lua, lua/*.lua, plugin manager markers (lazy.nvim bootstrap, packadd, mini.deps, vim-plug, etc)
- Identify what is already handled by mini.nvim vs external plugins
- Note any documented keymaps or constraints (README/AGENTS/docs)

### 3) Choose A Structure

Prefer a modular layout:

- init.lua: leader + bootstrap + load options/plugins/keymaps
- lua/options/*.lua: editor behavior, UI, keymaps, per-project helpers
- lua/plugins/*.lua: one feature/plugin per file; each returns lazy.nvim spec tables

If the existing config is small, keep it small; avoid refactors the user did not ask for.

### 4) Bootstrap lazy.nvim

Use the template in `references/templates.md`.

Rules:

- Clone lazy.nvim into `stdpath('data') .. '/lazy/lazy.nvim'`
- Prepend runtimepath
- Call `require('lazy').setup(...)` once
- Keep `lazy-lock.json` in the config root (default) unless the user asks otherwise

### 5) Configure mini.nvim

Two common approaches:

- Single plugin spec that calls multiple `mini.*.setup()` modules
- Split mini modules across multiple plugin spec files (e.g. `lua/plugins/mini_files.lua`)

Use `references/mini-modules.md` for suggested defaults and keymaps.

### 6) Add Baseline Plugins (optional)

Only add what the user wants. Common additions:

- LSP: `neovim/nvim-lspconfig` (+ `williamboman/mason.nvim` if they want installers)
- Treesitter: `nvim-treesitter/nvim-treesitter`
- Formatting: `stevearc/conform.nvim`
- Lint: `mfussenegger/nvim-lint`

If you add keymaps/commands, document them (either in repo docs or an in-config help section).

### 7) Validate / Smoke Test

Ask the user how they want to test (since this is a config repo):

- Start Neovim and ensure no startup errors
- Run `:Lazy` / `:Lazy sync` and restart
- Run `:checkhealth` and confirm no new critical errors

## Practices

- Keep plugin-specific keymaps close to the plugin spec.
- Prefer `opts = {}` + `config = function(_, opts) ... end` patterns for clarity.
- Avoid mixing plugin managers (lazy.nvim + mini.deps) unless the user explicitly wants it.

## References

- `references/templates.md`: copy-pastable skeletons (init.lua, lazy bootstrap, lua/plugins layout)
- `references/mini-modules.md`: mini.nvim module recipes and sensible defaults
- `references/migration.md`: migrating from packadd/mini.deps (high-level checklist)
