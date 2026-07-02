/**
 * Copy to: components/design-tweaks/applyCandidate.ts
 */

import type { DesignCandidate } from './candidates';

const STORAGE_KEY = 'design-tweaks:candidate';

let lastAppliedCandidate: DesignCandidate | null = null;

function clearCandidateFromRoot(candidate: DesignCandidate): void {
  const root = document.documentElement;

  for (const key of Object.keys(candidate.vars)) {
    root.style.removeProperty(key);
  }

  if (candidate.attrs) {
    for (const key of Object.keys(candidate.attrs)) {
      root.removeAttribute(key);
    }
  }
}

export function readStoredCandidateId(fallback: string): string {
  if (typeof window === 'undefined') return fallback;
  return localStorage.getItem(STORAGE_KEY) ?? fallback;
}

export function applyDesignCandidate(candidate: DesignCandidate): void {
  const root = document.documentElement;

  if (lastAppliedCandidate) {
    clearCandidateFromRoot(lastAppliedCandidate);
  }

  root.setAttribute('data-tweak-candidate', candidate.id);

  if (candidate.attrs) {
    for (const [key, value] of Object.entries(candidate.attrs)) {
      root.setAttribute(key, value);
    }
  }

  for (const [key, value] of Object.entries(candidate.vars)) {
    root.style.setProperty(key, value);
  }

  localStorage.setItem(STORAGE_KEY, candidate.id);
  lastAppliedCandidate = candidate;
}
