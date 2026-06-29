# デフォルト デザイントークン

Tailwind CSS v3 ベースのデフォルトデザインシステム。
プロジェクト固有のトークンがある場合はそちらを優先する。

---

## カラーシステム

### セマンティックカラー（`tailwind.config.js` で定義推奨）

```js
// tailwind.config.js
colors: {
  primary:   { 50:'#eff6ff', 100:'#dbeafe', 500:'#3b82f6', 600:'#2563eb', 700:'#1d4ed8', 900:'#1e3a8a' },
  secondary: { 50:'#f8fafc', 100:'#f1f5f9', 500:'#64748b', 600:'#475569', 700:'#334155', 900:'#0f172a' },
  success:   { 50:'#f0fdf4', 500:'#22c55e', 600:'#16a34a', 700:'#15803d' },
  warning:   { 50:'#fffbeb', 500:'#f59e0b', 600:'#d97706', 700:'#b45309' },
  error:     { 50:'#fef2f2', 500:'#ef4444', 600:'#dc2626', 700:'#b91c1c' },
  neutral:   { 50:'#fafafa', 100:'#f5f5f5', 200:'#e5e5e5', 300:'#d4d4d4', 400:'#a3a3a3', 500:'#737373', 600:'#525252', 700:'#404040', 800:'#262626', 900:'#171717' },
}
```

### 用途マッピング

| 用途 | Light | Dark |
|------|-------|------|
| ページ背景 | `bg-white` / `bg-neutral-50` | `dark:bg-neutral-900` |
| カード背景 | `bg-white` | `dark:bg-neutral-800` |
| プライマリテキスト | `text-neutral-900` | `dark:text-neutral-50` |
| セカンダリテキスト | `text-neutral-600` | `dark:text-neutral-400` |
| ボーダー | `border-neutral-200` | `dark:border-neutral-700` |
| CTA（主要アクション）| `bg-primary-600` | `dark:bg-primary-500` |

---

## タイポグラフィ

### フォントスケール

```
text-xs    → 12px / lh 1.5  → ラベル、キャプション
text-sm    → 14px / lh 1.5  → 補助テキスト、フォームヒント
text-base  → 16px / lh 1.75 → 本文（基準）
text-lg    → 18px / lh 1.75 → リードテキスト
text-xl    → 20px / lh 1.5  → セクション見出し
text-2xl   → 24px / lh 1.25 → H3
text-3xl   → 30px / lh 1.25 → H2
text-4xl   → 36px / lh 1.1  → H1（ページタイトル）
```

### フォントウェイト

```
font-normal   (400) → 本文
font-medium   (500) → UIラベル、ボタン
font-semibold (600) → 見出し、強調
font-bold     (700) → 大見出し
```

### 推奨フォントスタック

```js
fontFamily: {
  sans: ['Inter', 'Noto Sans JP', 'ui-sans-serif', 'system-ui'],
  mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
}
```

---

## スペーシング

Tailwind デフォルトスケール（4px基数）に準拠。

| Token | px | 用途 |
|-------|-----|------|
| `p-1` | 4px | アイコンパディング等の微調整 |
| `p-2` | 8px | コンパクトなUI要素 |
| `p-3` | 12px | 小〜中ボタン、インプット |
| `p-4` | 16px | カード内パディング（標準） |
| `p-6` | 24px | セクション内パディング |
| `p-8` | 32px | ページセクション |
| `gap-4` | 16px | リスト・グリッドの標準ギャップ |
| `gap-6` | 24px | カードグリッドのギャップ |

---

## ボーダーとシャドウ

```
rounded-sm   → 2px   小アイコン・タグ
rounded      → 4px   インプット、セレクト
rounded-md   → 6px   ボタン（標準）
rounded-lg   → 8px   カード
rounded-xl   → 12px  モーダル
rounded-2xl  → 16px  大きなカード
rounded-full → 9999px ピル、アバター

shadow-sm  → 微妙な影（カード）
shadow     → 標準的な影（ドロップダウン）
shadow-md  → 浮き上がり感（ポップアップ）
shadow-lg  → モーダル、ダイアログ
```

---

## ブレークポイント（Responsive）

Mobile-first で設計する。

```
sm:  640px  → スマートフォン横持ち
md:  768px  → タブレット縦
lg:  1024px → タブレット横 / 小デスクトップ
xl:  1280px → デスクトップ
2xl: 1536px → 大画面
```

**コンテナ幅**:
```
max-w-sm   → 384px  狭いフォーム
max-w-md   → 448px  モーダル
max-w-lg   → 512px  コンテンツカラム
max-w-2xl  → 672px  記事・ドキュメント
max-w-4xl  → 896px  ダッシュボード
max-w-7xl  → 1280px ページコンテナ
```

---

## アニメーション

```
transition-colors   duration-150 → ホバー・フォーカスのカラー変化
transition-opacity  duration-200 → フェードイン/アウト
transition-all      duration-200 → 汎用（多用しない）
animate-spin        → ローディングスピナー
animate-pulse       → スケルトンローディング
```

標準イージング: `ease-in-out`（Tailwind デフォルト）
