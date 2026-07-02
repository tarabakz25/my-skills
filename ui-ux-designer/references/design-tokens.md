# Default Design Tokens

Default design system based on Tailwind CSS v3.
Prefer project-specific tokens when they already exist.

---

## Color System

### Semantic Colors (recommended in `tailwind.config.js`)

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

### Usage Mapping

| Usage | Light | Dark |
|-------|-------|------|
| Page background | `bg-white` / `bg-neutral-50` | `dark:bg-neutral-900` |
| Card background | `bg-white` | `dark:bg-neutral-800` |
| Primary text | `text-neutral-900` | `dark:text-neutral-50` |
| Secondary text | `text-neutral-600` | `dark:text-neutral-400` |
| Border | `border-neutral-200` | `dark:border-neutral-700` |
| CTA (primary action) | `bg-primary-600` | `dark:bg-primary-500` |

---

## Typography

### Font Scale

```
text-xs    → 12px / lh 1.5  → labels, captions
text-sm    → 14px / lh 1.5  → supporting text, form hints
text-base  → 16px / lh 1.75 → body (baseline)
text-lg    → 18px / lh 1.75 → lead text
text-xl    → 20px / lh 1.5  → section headings
text-2xl   → 24px / lh 1.25 → H3
text-3xl   → 30px / lh 1.25 → H2
text-4xl   → 36px / lh 1.1  → H1 (page title)
```

### Font Weights

```
font-normal   (400) → body
font-medium   (500) → UI labels, buttons
font-semibold (600) → headings, emphasis
font-bold     (700) → large headings
```

### Recommended Font Stack

```js
fontFamily: {
  sans: ['Inter', 'Noto Sans JP', 'ui-sans-serif', 'system-ui'],
  mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
}
```

---

## Spacing

Follows Tailwind default scale (4px base).

| Token | px | Usage |
|-------|-----|-------|
| `p-1` | 4px | Fine adjustments, icon padding |
| `p-2` | 8px | Compact UI elements |
| `p-3` | 12px | Small to medium buttons, inputs |
| `p-4` | 16px | Standard card padding |
| `p-6` | 24px | Section padding |
| `p-8` | 32px | Page sections |
| `gap-4` | 16px | Standard list/grid gap |
| `gap-6` | 24px | Card grid gap |

---

## Borders and Shadows

```
rounded-sm   → 2px   small icons, tags
rounded      → 4px   inputs, selects
rounded-md   → 6px   buttons (standard)
rounded-lg   → 8px   cards
rounded-xl   → 12px  modals
rounded-2xl  → 16px  large cards
rounded-full → 9999px pills, avatars

shadow-sm  → subtle shadow (cards)
shadow     → standard shadow (dropdowns)
shadow-md  → elevated feel (popovers)
shadow-lg  → modals, dialogs
```

---

## Breakpoints (Responsive)

Design mobile-first.

```
sm:  640px  → landscape phone
md:  768px  → portrait tablet
lg:  1024px → landscape tablet / small desktop
xl:  1280px → desktop
2xl: 1536px → large screen
```

**Container widths**:
```
max-w-sm   → 384px  narrow forms
max-w-md   → 448px  modals
max-w-lg   → 512px  content columns
max-w-2xl  → 672px  articles, docs
max-w-4xl  → 896px  dashboards
max-w-7xl  → 1280px page containers
```

---

## Animation

```
transition-colors   duration-150 → hover/focus color changes
transition-opacity  duration-200 → fade in/out
transition-all      duration-200 → general use (do not overuse)
animate-spin        → loading spinner
animate-pulse       → skeleton loading
```

Default easing: `ease-in-out` (Tailwind default)
