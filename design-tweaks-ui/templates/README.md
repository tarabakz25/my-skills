# Integration Guide

Copy templates from this directory into the target project.

## 1. Copy files

```bash
mkdir -p components/design-tweaks
cp ~/.skills/design-tweaks-ui/templates/candidates.example.ts components/design-tweaks/candidates.ts
cp ~/.skills/design-tweaks-ui/templates/applyCandidate.ts components/design-tweaks/
cp ~/.skills/design-tweaks-ui/templates/useDesignTweaks.ts components/design-tweaks/
cp ~/.skills/design-tweaks-ui/templates/DesignTweaksProvider.tsx components/design-tweaks/
cp ~/.skills/design-tweaks-ui/templates/DesignTweaksPanel.tsx components/design-tweaks/
cp ~/.skills/design-tweaks-ui/templates/globals.tweaks.css styles/design-tweaks.css
```

## 2. Import CSS

```css
/* app/globals.css */
@import '../styles/design-tweaks.css';
```

## 3. Wrap layout (one change)

```tsx
// app/layout.tsx
import { DesignTweaksProvider } from '@/components/design-tweaks/DesignTweaksProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <DesignTweaksProvider>{children}</DesignTweaksProvider>
      </body>
    </html>
  );
}
```

## 4. Tokenize comparison targets (minimal)

Replace hardcoded colors on components you want to compare:

```tsx
// Before
<main className="bg-white text-slate-900">

// After — keep structure, swap to token utilities
<main className="bg-surface text-primary app-shell">
```

## 5. Add candidates

Edit `components/design-tweaks/candidates.ts` only. Each new button = one array entry.

## 6. Verify

```bash
npm run dev
# Click "Tweaks" FAB → switch candidates → confirm colors/layout change
# Reload → last candidate restores
NODE_ENV=production npm run build
# Confirm panel absent unless NEXT_PUBLIC_DESIGN_TWEAKS=1
```

## CRA / Vite (no Next dynamic)

Replace `DesignTweaksProvider.tsx` with:

```tsx
import { lazy, Suspense, type ReactNode } from 'react';

const DesignTweaksPanel = lazy(() =>
  import('./DesignTweaksPanel').then((m) => ({ default: m.DesignTweaksPanel })),
);

export function DesignTweaksProvider({ children }: { children: ReactNode }) {
  const enabled =
    import.meta.env.DEV || import.meta.env.VITE_DESIGN_TWEAKS === '1';
  return (
    <>
      {children}
      {enabled ? (
        <Suspense fallback={null}>
          <DesignTweaksPanel />
        </Suspense>
      ) : null}
    </>
  );
}
```
