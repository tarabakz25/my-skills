'use client';

/**
 * Copy to: components/design-tweaks/useDesignTweaks.ts
 */

import { useCallback, useEffect, useState } from 'react';
import { applyDesignCandidate, readStoredCandidateId } from './applyCandidate';
import {
  DEFAULT_CANDIDATE_ID,
  DESIGN_CANDIDATES,
  getCandidateById,
  type DesignCandidate,
} from './candidates';

export function useDesignTweaks() {
  const [candidateId, setCandidateIdState] = useState(DEFAULT_CANDIDATE_ID);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const id = readStoredCandidateId(DEFAULT_CANDIDATE_ID);
    const candidate = getCandidateById(id) ?? getCandidateById(DEFAULT_CANDIDATE_ID);
    if (candidate) {
      applyDesignCandidate(candidate);
      setCandidateIdState(candidate.id);
    }
  }, []);

  const setCandidate = useCallback((id: string) => {
    const candidate = getCandidateById(id);
    if (!candidate) return;
    applyDesignCandidate(candidate);
    setCandidateIdState(id);
  }, []);

  const reset = useCallback(() => {
    setCandidate(DEFAULT_CANDIDATE_ID);
  }, [setCandidate]);

  return {
    candidates: DESIGN_CANDIDATES as DesignCandidate[],
    candidateId,
    setCandidate,
    reset,
    open,
    setOpen,
  };
}
