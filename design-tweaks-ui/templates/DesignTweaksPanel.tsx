'use client';

/**
 * Copy to: components/design-tweaks/DesignTweaksPanel.tsx
 * Floating popup — candidate switch via buttons.
 */

import { useEffect, useRef } from 'react';
import { useDesignTweaks } from './useDesignTweaks';

export function DesignTweaksPanel() {
  const { candidates, candidateId, setCandidate, reset, open, setOpen } =
    useDesignTweaks();
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') setOpen(false);
    }

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open, setOpen]);

  return (
    <>
      <button
        type="button"
        aria-label="Open design tweaks"
        aria-expanded={open}
        aria-controls="design-tweaks-panel"
        onClick={() => setOpen((v) => !v)}
        className="design-tweaks-fab"
      >
        Tweaks
      </button>

      {open ? (
        <div
          id="design-tweaks-panel"
          ref={panelRef}
          role="dialog"
          aria-modal="false"
          aria-label="Design candidate comparison"
          className="design-tweaks-panel"
        >
          <header className="design-tweaks-header">
            <div>
              <p className="design-tweaks-title">Design candidates</p>
              <p className="design-tweaks-subtitle">
                Switch layout, color, and density
              </p>
            </div>
            <button
              type="button"
              className="design-tweaks-close"
              aria-label="Close design tweaks"
              onClick={() => setOpen(false)}
            >
              ×
            </button>
          </header>

          <div className="design-tweaks-list" role="group" aria-label="Candidates">
            {candidates.map((c) => {
              const active = c.id === candidateId;
              return (
                <button
                  key={c.id}
                  type="button"
                  aria-pressed={active}
                  onClick={() => setCandidate(c.id)}
                  className={`design-tweaks-candidate${active ? ' is-active' : ''}`}
                >
                  <span className="design-tweaks-candidate-label">{c.label}</span>
                  {c.description ? (
                    <span className="design-tweaks-candidate-desc">{c.description}</span>
                  ) : null}
                </button>
              );
            })}
          </div>

          <footer className="design-tweaks-footer">
            <button type="button" className="design-tweaks-reset" onClick={reset}>
              Reset to baseline
            </button>
          </footer>
        </div>
      ) : null}
    </>
  );
}
