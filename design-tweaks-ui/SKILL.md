---
name: design-tweaks-ui
description: "Use when adding a dev-only tweaks popup to compare design candidates (layout, color, typography, spacing) via buttons without modifying existing UI code. Covers CSS-variable presets, React provider pattern, candidate switching, and safe integration with Tailwind/Next.js."
version: 1.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ui, design, tweaks, devtools, react, tailwind, theming]
    related_skills: [ui-ux-designer, frontend-design, design-system, browser-qa]
---

# Design Tweaks UI

## Overview

既存 UI を書き換えずに、**デザイン候補（レイアウト・カラー・タイポ・スペーシング等）をボタンで切り替えて比較**するための dev-only ポップアップ UI を追加するスキル。

**コア哲学**: 既存コンポーネントは触らない。候補は **CSS 変数 + data 属性** で外側から注入し、Tweaks パネルだけが候補定義と切替ロジックを持つ。

**優先順位**:
1. 既存コード非破壊（追加ファイル中心、既存は CSS 変数参照に寄せる最小 diff のみ）
2. 候補切替の即時性（ボタン 1 クリックで全体反映）
3. dev-only 分離（本番バンドルから除外可能）
4. a11y（パネル自体もキーボード操作可能）

## When to Use

**Use this skill when:**
- 複数のデザイン案（配色・レイアウト・密度・角丸等）を並べて比較したい
- 既存画面を壊さずに Tweaks ポップアップを足したい
- React/Next.js + Tailwind プロジェクトで候補プリセットを試したい
- デザインレビュー前にステークホルダーが候補を切り替えて見たい

**Don't use for:**
- 本番ユーザー向けテーマ切替（設定画面・ダークモード）→ プロジェクトの theme 実装を使う
- デザインシステム全体の監査・トークン生成 → `design-system`
- 初回ビジュアル方向の探索のみ → `frontend-design` を先に
- E2E テスト・a11y 監査 → `browser-qa` / `accessibility`

## アーキテクチャ（非破壊）

```
┌─────────────────────────────────────────┐
│  <html data-tweak-candidate="b">        │  ← 候補 ID を root に付与
│    CSS variables (--primary, --radius…) │  ← 候補ごとに上書き
│  ┌───────────────────────────────────┐  │
│  │  Existing App (変更最小)           │  │  ← var(--token) 参照のみ
│  └───────────────────────────────────┘  │
│  ┌─ TweaksPanel (dev-only, fixed) ───┐  │  ← 新規追加。候補ボタン
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

詳細 → [`references/architecture.md`](references/architecture.md)

## ワークフロー

### 1. 既存コードを読む（変更前）

- ページ root / layout の場所を特定
- ハードコード色（`bg-[#...]`、`text-blue-600` 等）を洗い出す
- プロジェクトに CSS 変数や `tailwind.config` トークンがあるか確認

**ルール**: 候補比較に必要な箇所だけ `var(--token)` 化。一括 refactor はしない。

### 2. 候補定義を作る

`candidates.ts` にプリセットを集約。1 候補 = 1 オブジェクト。

```ts
export type DesignCandidate = {
  id: string;
  label: string;
  description?: string;
  vars: Record<string, string>;      // CSS custom properties
  attrs?: Record<string, string>;    // e.g. data-layout="compact"
};
```

テンプレート → [`templates/candidates.example.ts`](templates/candidates.example.ts)

**候補の粒度**（混在 OK）:
| 軸 | 例 vars / attrs |
|----|-----------------|
| カラー | `--primary`, `--surface`, `--text` |
| レイアウト | `data-layout="sidebar"` / `"centered"` |
| タイポ | `--font-sans`, `--text-base` |
| 形状 | `--radius`, `--shadow` |
| 密度 | `--space-unit`, `data-density="compact"` |

### 3. Provider + root 属性を追加

既存 layout を **ラップするだけ**。中身は書き換えない。

```tsx
// app/layout.tsx または _app.tsx — 末尾に 1 行追加するイメージ
import { DesignTweaksProvider } from '@/components/design-tweaks/DesignTweaksProvider';

export default function RootLayout({ children }) {
  return (
    <html lang="ja">
      <body>
        <DesignTweaksProvider>{children}</DesignTweaksProvider>
      </body>
    </html>
  );
}
```

テンプレート一式 → [`templates/`](templates/)

### 4. Tweaks ポップアップ UI を実装

必須 UI 要素:

| 要素 | 要件 |
|------|------|
| 起動ボタン | 画面端 fixed。`aria-label="Open design tweaks"` |
| 候補ボタン群 | 現在候補を `aria-pressed` で表示 |
| 候補ラベル | `label` + 任意 `description` |
| 閉じる | Esc / オーバーレイ外クリック / Close ボタン |
| リセット | デフォルト候補に戻す |

**切替ロジック**:
1. ボタン click → `setCandidate(id)`
2. `document.documentElement` に `data-tweak-candidate` と CSS vars を apply
3. `localStorage` に保存（キー: `design-tweaks:candidate`）
4. 初回 mount で restore

### 5. 既存スタイルを token 参照に寄せる（最小 diff）

```tsx
// Before（候補切替不可）
<div className="bg-blue-600 rounded-lg p-4">

// After（候補切替可能 — class 構造は維持）
<div
  className="rounded-lg p-4"
  style={{ backgroundColor: 'var(--primary)', borderRadius: 'var(--radius-md)' }}
>

// または globals.css で utility を定義
// .bg-token-primary { background-color: var(--primary); }
```

Tailwind プロジェクトでは [`templates/globals.tweaks.css`](templates/globals.tweaks.css) を `@import` する。

### 6. dev-only でガード

```tsx
const enabled =
  process.env.NODE_ENV === 'development' ||
  process.env.NEXT_PUBLIC_DESIGN_TWEAKS === '1';

if (!enabled) return <>{children}</>;
```

Next.js: `DesignTweaksPanel` を `dynamic(() => import(...), { ssr: false })` で遅延読込し、本番 tree-shake を助ける。

### 7. 比較レビュー

候補ごとに以下を記録（メモ欄をパネルに付けてもよい）:

- 375px / 768px / 1280px でレイアウト崩れ
- コントラスト（WCAG AA）
- 主要フロー 3 クリック以内か
- 採用候補 ID と理由

→ [`references/review-checklist.md`](references/review-checklist.md)

## ファイル追加チェックリスト

新規追加（既存を壊さない）:

```
components/design-tweaks/
  candidates.ts          # 候補定義（プロジェクト固有）
  applyCandidate.ts      # DOM apply ユーティリティ
  DesignTweaksProvider.tsx
  DesignTweaksPanel.tsx  # ポップアップ UI
  useDesignTweaks.ts     # hook（任意）
styles/
  design-tweaks.css      # パネル用 + token utilities（任意）
```

既存への変更は **layout 1 行の wrap** と **比較対象コンポーネントの token 化** に限定。

## Common Pitfalls

1. **既存 className を候補ごとに分岐** — 保守不能。CSS 変数 + data 属性に統一する。

2. **候補定義を Panel 内に直書き** — `candidates.ts` に分離しないと diff が読めない。

3. **本番に Tweaks を出す** — `NODE_ENV` / feature flag 必須。本番テーマ切替は別実装。

4. **root 以外に vars を apply** — `document.documentElement` のみ。子要素個別は漏れる。

5. **ハードコード色のまま比較** — 切替しても変わらない。比較対象だけ `var(--*)` 化。

6. **パネルが既 UI を覆いすぎ** — `z-index` は `9999` 程度、幅は `max-w-sm`、ドラッグ可能にするとよい。

7. **候補 ID をラベルと混同** — `id` は安定 kebab-case、`label` は表示名。

8. **SSR で localStorage 参照** — mount 後のみ restore。Provider 内 `useEffect` で apply。

## Verification Checklist

- [ ] 既存コンポーネントのロジック・構造を変更していない（スタイル token 化のみ）
- [ ] 候補ボタンで **即座に** 全体の色・レイアウト属性が切り替わる
- [ ] リロード後も最後の候補が restore される（dev のみ）
- [ ] `NODE_ENV=production` ビルドに Tweaks パネルが含まれない（または flag off で非表示）
- [ ] パネルが Tab / Esc / Enter で操作できる
- [ ] 375px 幅でパネルが画面外にはみ出さない
- [ ] 採用候補の vars を `design-tokens` / Tailwind config へ昇格する手順をメモした

### Frontmatter 検証（スキル更新時）

```bash
python3 -c "
import yaml, re, pathlib
p = pathlib.Path('~/.skills/design-tweaks-ui/SKILL.md').expanduser()
content = p.read_text()
assert content.startswith('---'), 'Must start with ---'
m = re.search(r'\n---\s*\n', content[3:])
fm = yaml.safe_load(content[3:m.start()+3])
assert fm['name'] == 'design-tweaks-ui'
assert len(fm['description']) <= 1024
assert len(content) <= 100_000
print('OK:', fm['version'])
"
```

## 追加リソース

| ファイル | 内容 |
|---------|------|
| [`references/architecture.md`](references/architecture.md) | 非破壊統合・data 属性戦略 |
| [`references/review-checklist.md`](references/review-checklist.md) | 候補比較レビュー |
| [`templates/`](templates/) | コピー可能な React/CSS テンプレート |
