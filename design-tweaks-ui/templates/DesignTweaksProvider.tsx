'use client';

/**
 * Copy to: components/design-tweaks/DesignTweaksProvider.tsx
 * Wrap existing layout children — do not modify children.
 */

import dynamic from 'next/dynamic';
import { type ReactNode } from 'react';

const DesignTweaksPanel = dynamic(
  () => import('./DesignTweaksPanel').then((m) => m.DesignTweaksPanel),
  { ssr: false },
);

function isTweaksEnabled(): boolean {
  return (
    process.env.NODE_ENV === 'development' ||
    process.env.NEXT_PUBLIC_DESIGN_TWEAKS === '1'
  );
}

export function DesignTweaksProvider({ children }: { children: ReactNode }) {
  const enabled = isTweaksEnabled();

  return (
    <>
      {children}
      {enabled ? <DesignTweaksPanel /> : null}
    </>
  );
}
