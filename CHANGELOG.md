# Changelog

## [project-init 1.0.0] - 2026-06-29

### Added
- `~/.skills/project-init/` — analyze a project codebase and generate missing `README.md` and/or `CLAUDE.md`
- `scripts/detect_project.py` — manifest/stack/command recon helper
- Output templates for README and CLAUDE structure
- Root `~/.skills/README.md` and `~/.skills/CLAUDE.md` — generated via `/project-init` for the skills library itself

### Removed
- `~/.skills/skill-init/` — wrong scope (was for ~/.skills scaffolding, not project init)

## [repo] - 2026-06-29

### Added
- `~/.claude/skills/`・`~/.cursor/skills/`・`~/.codex/skills/` から重複を除き **217 件**を `.skills/` 直下に集約（既存 4 件 + 新規 213 件、計 219 `SKILL.md`）。
- `.codex/skills/.system/` の 5 件は `.system/` 配下に配置。
- ソース間で名前が重なるスキルは `.claude` > `.cursor` > `.codex` の優先順位で採用。

## [spec 2.3.0] - 2026-06-29

### Changed
- `/spec create`: 要件サイズ（minimal / standard / full）に応じてセクションを選択する Phase 1.5 Sizing を追加。固定サイズの全セクション出力を廃止。
- `/spec create`: 技術的実現性・不明点をユーザー確認する Phase 1.6 Feasibility Gate を追加。ブロッカー未解決時はドラフト保存しない。
- `references/section-catalog.md` を新規追加。タイプ別・複雑度別のセクション包含基準を定義。

### Fixed
- 公式 API / プラットフォームで未提供の機能（例: Cursor ACP の max mode）を spec にそのまま書いてしまう問題を、調査 → 確認 → 代替案提示のフローで防止。
