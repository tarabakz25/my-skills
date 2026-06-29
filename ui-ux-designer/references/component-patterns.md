# UIコンポーネント実装パターン

Tailwind CSS + React 18 ベースの標準パターン集。
shadcn/ui や Radix UI が利用可能な場合は積極的に活用する（アクセシビリティ対応済み）。

---

## TOC

1. [Button](#button)
2. [Input / Form](#input--form)
3. [Card](#card)
4. [Navigation (Navbar / Sidebar)](#navigation)
5. [Modal / Dialog](#modal--dialog)
6. [Alert / Toast](#alert--toast)
7. [Table](#table)
8. [Loading States](#loading-states)
9. [Empty State](#empty-state)
10. [Avatar / Badge](#avatar--badge)

---

## Button

### バリアント定義

```tsx
const variants = {
  primary:   'bg-primary-600 hover:bg-primary-700 text-white',
  secondary: 'bg-white hover:bg-neutral-50 text-neutral-700 border border-neutral-300',
  ghost:     'hover:bg-neutral-100 text-neutral-700',
  danger:    'bg-error-600 hover:bg-error-700 text-white',
  link:      'text-primary-600 hover:text-primary-700 underline-offset-4 hover:underline',
}
const sizes = {
  sm: 'px-3 py-1.5 text-xs rounded',
  md: 'px-4 py-2 text-sm rounded-md',    // デフォルト
  lg: 'px-6 py-3 text-base rounded-lg',
}
const base = 'inline-flex items-center gap-2 font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none'
```

```tsx
// 使用例
<button className={`${base} ${variants.primary} ${sizes.md}`}>
  <PlusIcon className="w-4 h-4" />
  作成する
</button>

// ローディング状態
<button disabled className={`${base} ${variants.primary} ${sizes.md}`}>
  <Spinner className="w-4 h-4 animate-spin" />
  保存中...
</button>
```

---

## Input / Form

```tsx
// テキストインプット
<div className="space-y-1.5">
  <label htmlFor="email" className="block text-sm font-medium text-neutral-700">
    メールアドレス
  </label>
  <input
    id="email"
    type="email"
    placeholder="you@example.com"
    className="block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm
               placeholder-neutral-400 shadow-sm
               focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500
               disabled:bg-neutral-50 disabled:text-neutral-500"
  />
  {/* エラー時 */}
  <p className="text-xs text-error-600" role="alert">有効なメールアドレスを入力してください</p>
</div>
```

```tsx
// セレクト
<select className="block w-full rounded-md border border-neutral-300 bg-white px-3 py-2 text-sm
                   focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500">
  <option value="">選択してください</option>
</select>
```

```tsx
// フォームレイアウト（2カラム）
<form className="grid grid-cols-1 gap-6 sm:grid-cols-2">
  {/* フルワイズフィールドは col-span-2 */}
</form>
```

---

## Card

```tsx
// 基本カード
<div className="rounded-lg border border-neutral-200 bg-white p-6 shadow-sm">
  <h3 className="text-base font-semibold text-neutral-900">タイトル</h3>
  <p className="mt-1 text-sm text-neutral-600">説明テキスト</p>
</div>

// クリッカブルカード（ホバー効果）
<div className="group rounded-lg border border-neutral-200 bg-white p-6 shadow-sm
                cursor-pointer transition-shadow hover:shadow-md hover:border-neutral-300">
</div>

// メトリクスカード（ダッシュボード用）
<div className="rounded-lg border border-neutral-200 bg-white p-6">
  <p className="text-sm font-medium text-neutral-600">総ユーザー数</p>
  <p className="mt-2 text-3xl font-semibold text-neutral-900">12,345</p>
  <p className="mt-1 text-sm text-success-600">+12% 先月比</p>
</div>
```

---

## Navigation

### Topbar (Desktop)

```tsx
<nav className="sticky top-0 z-40 border-b border-neutral-200 bg-white">
  <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
    <div className="flex items-center gap-8">
      <Logo />
      <div className="hidden md:flex items-center gap-1">
        {navItems.map(item => (
          <a key={item.href} href={item.href}
             className="rounded-md px-3 py-2 text-sm font-medium text-neutral-600
                        hover:bg-neutral-100 hover:text-neutral-900
                        aria-[current=page]:bg-primary-50 aria-[current=page]:text-primary-700">
            {item.label}
          </a>
        ))}
      </div>
    </div>
    <div className="flex items-center gap-3">
      {/* Actions */}
    </div>
  </div>
</nav>
```

### Sidebar (Dashboard)

```tsx
<aside className="fixed inset-y-0 left-0 z-30 w-64 border-r border-neutral-200 bg-white">
  <div className="flex h-16 items-center border-b border-neutral-200 px-6">
    <Logo />
  </div>
  <nav className="p-4 space-y-1">
    {navItems.map(item => (
      <a key={item.href} href={item.href}
         className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium
                    text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900
                    aria-[current=page]:bg-primary-50 aria-[current=page]:text-primary-700">
        <item.icon className="w-5 h-5" />
        {item.label}
      </a>
    ))}
  </nav>
</aside>
```

---

## Modal / Dialog

Radix UI の `Dialog` を使う（アクセシビリティ対応済み）。

```tsx
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Root open={open} onOpenChange={setOpen}>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm
                                data-[state=open]:animate-in data-[state=closed]:animate-out
                                data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
    <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-md
                                -translate-x-1/2 -translate-y-1/2
                                rounded-xl bg-white p-6 shadow-lg
                                data-[state=open]:animate-in data-[state=closed]:animate-out
                                data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
      <div className="flex items-start justify-between">
        <Dialog.Title className="text-lg font-semibold text-neutral-900">
          タイトル
        </Dialog.Title>
        <Dialog.Close className="rounded-md p-1 text-neutral-400 hover:text-neutral-600">
          <XIcon className="w-5 h-5" />
        </Dialog.Close>
      </div>
      <Dialog.Description className="mt-2 text-sm text-neutral-600">
        説明
      </Dialog.Description>
      {/* Content */}
      <div className="mt-6 flex justify-end gap-3">
        <Dialog.Close asChild>
          <button className={secondaryBtn}>キャンセル</button>
        </Dialog.Close>
        <button className={primaryBtn}>確定</button>
      </div>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

---

## Alert / Toast

```tsx
// インラインアラート
const alertStyles = {
  info:    'bg-primary-50 border-primary-200 text-primary-800',
  success: 'bg-success-50 border-success-200 text-success-800',
  warning: 'bg-warning-50 border-warning-200 text-warning-800',
  error:   'bg-error-50 border-error-200 text-error-800',
}
<div role="alert" className={`rounded-lg border p-4 text-sm ${alertStyles.error}`}>
  <div className="flex gap-3">
    <AlertIcon className="mt-0.5 w-4 h-4 shrink-0" />
    <p>エラーメッセージ</p>
  </div>
</div>

// Toast（react-hot-toast または sonner を推奨）
import { toast } from 'sonner'
toast.success('保存しました')
toast.error('エラーが発生しました')
```

---

## Table

```tsx
<div className="overflow-hidden rounded-lg border border-neutral-200">
  <table className="min-w-full divide-y divide-neutral-200">
    <thead className="bg-neutral-50">
      <tr>
        {columns.map(col => (
          <th key={col.key} scope="col"
              className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-neutral-500">
            {col.label}
          </th>
        ))}
      </tr>
    </thead>
    <tbody className="divide-y divide-neutral-100 bg-white">
      {rows.map(row => (
        <tr key={row.id} className="hover:bg-neutral-50 transition-colors">
          <td className="px-4 py-3 text-sm text-neutral-900">{row.name}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

---

## Loading States

```tsx
// スピナー
<div role="status" aria-label="読み込み中">
  <svg className="w-6 h-6 animate-spin text-primary-600" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
  </svg>
</div>

// スケルトンローダー
<div className="animate-pulse space-y-3">
  <div className="h-4 w-3/4 rounded bg-neutral-200" />
  <div className="h-4 w-1/2 rounded bg-neutral-200" />
  <div className="h-32 w-full rounded-lg bg-neutral-200" />
</div>
```

---

## Empty State

```tsx
<div className="flex flex-col items-center justify-center py-16 text-center">
  <IllustrationIcon className="w-16 h-16 text-neutral-300" />
  <h3 className="mt-4 text-base font-semibold text-neutral-900">データがありません</h3>
  <p className="mt-1 text-sm text-neutral-500">
    最初のアイテムを作成してください。
  </p>
  <button className={`mt-6 ${primaryBtn}`}>
    <PlusIcon className="w-4 h-4" />
    作成する
  </button>
</div>
```

---

## Avatar / Badge

```tsx
// アバター
<span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-primary-100">
  <span className="text-sm font-medium text-primary-700">KZ</span>
</span>

// バッジ
const badgeStyles = {
  gray:    'bg-neutral-100 text-neutral-700',
  blue:    'bg-primary-50 text-primary-700',
  green:   'bg-success-50 text-success-700',
  yellow:  'bg-warning-50 text-warning-700',
  red:     'bg-error-50 text-error-700',
}
<span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${badgeStyles.green}`}>
  アクティブ
</span>
```
