# Design Tweaks UI — Architecture

## 非破壊統合の原則

| 層 | 触る | 触らない |
|----|------|----------|
| 候補定義 | 新規 `candidates.ts` | — |
| 適用ロジック | 新規 `applyCandidate.ts` | — |
| UI シェル | 新規 `DesignTweaksPanel` | 既存ページ JSX 構造 |
| スタイル | CSS 変数参照へ **最小** 置換 | レイアウト grid/flex 構造の書き換え |
| Layout | Provider で **wrap のみ** | children の中身 |

## 候補の適用順序

1. `document.documentElement.setAttribute('data-tweak-candidate', id)`
2. 候補 `attrs` を root に merge（`data-layout`, `data-density` 等）
3. 候補 `vars` を `style.setProperty('--key', value)` で apply
4. `localStorage.setItem('design-tweaks:candidate', id)`

## CSS 変数 vs data 属性

| 用途 | 手段 | 例 |
|------|------|-----|
| 色・フォント・半径・影 | CSS variables | `--primary: #2563eb` |
| レイアウトモード | data 属性 + CSS セレクタ | `[data-layout="sidebar"] .main { ... }` |
| コンポーネント密度 | data 属性 | `[data-density="compact"] { --space-unit: 0.75rem }` |

```css
/* globals または design-tweaks.css */
[data-layout="centered"] .app-shell {
  max-width: 48rem;
  margin-inline: auto;
}

[data-layout="wide"] .app-shell {
  max-width: 80rem;
}

[data-density="compact"] {
  --space-unit: 0.75rem;
}

[data-density="comfortable"] {
  --space-unit: 1rem;
}
```

既存コンポーネントは `.app-shell` 等の **既存 class を維持**し、layout 差分は data 属性セレクタだけで表現する。

## Tailwind との共存

### 推奨: semantic token utilities

```css
.bg-surface { background-color: var(--surface); }
.text-primary { color: var(--text-primary); }
.rounded-token { border-radius: var(--radius-md); }
```

Tailwind の `@layer utilities` に追加。既存 `className` の utility 名を token 版に **1:1 置換**するだけ。

### 非推奨: 候補ごとに Tailwind class を切替

```tsx
// Bad — 候補追加のたびに JSX 分岐が増える
className={candidate === 'a' ? 'bg-blue-600' : 'bg-violet-600'}
```

## Next.js App Router

```
app/
  layout.tsx          ← DesignTweaksProvider で wrap
  globals.css         ← @import design-tweaks.css
components/
  design-tweaks/      ← 新規ディレクトリのみ
```

`DesignTweaksPanel` は client component。Provider も client。

```tsx
// dynamic import で本番バンドル軽量化
const DesignTweaksPanel = dynamic(
  () => import('./DesignTweaksPanel').then(m => m.DesignTweaksPanel),
  { ssr: false }
);
```

## 候補の昇格フロー

比較完了後:

1. 採用候補 ID を決定
2. `candidates.ts` の vars をプロジェクトの `tailwind.config` / `:root` に写す
3. Tweaks 用の暫定 utility を正式トークン名へ rename
4. dev flag を off にして Tweaks ディレクトリを残す（再比較用）か削除するかを選ぶ

## z-index / ポータル

- パネル: `position: fixed; bottom: 1rem; right: 1rem; z-index: 9999`
- バックドロップ（任意）: `z-index: 9998`
- Radix Dialog を使う場合も **既存 Dialog より上**にするか、独立した fixed パネルを推奨（既存 Modal と競合しない）
