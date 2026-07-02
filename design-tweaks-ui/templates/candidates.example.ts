/**
 * Copy to: components/design-tweaks/candidates.ts
 * Edit vars/attrs per project. Do not embed in Panel component.
 */

export type DesignCandidate = {
  id: string;
  label: string;
  description?: string;
  vars: Record<string, string>;
  attrs?: Record<string, string>;
};

export const DEFAULT_CANDIDATE_ID = 'baseline';

export const DESIGN_CANDIDATES: DesignCandidate[] = [
  {
    id: 'baseline',
    label: 'Baseline',
    description: 'Current production tokens',
    vars: {
      '--primary': '#2563eb',
      '--primary-hover': '#1d4ed8',
      '--surface': '#ffffff',
      '--surface-muted': '#f8fafc',
      '--text-primary': '#0f172a',
      '--text-secondary': '#64748b',
      '--radius-sm': '0.375rem',
      '--radius-md': '0.5rem',
      '--radius-lg': '0.75rem',
      '--shadow-sm': '0 1px 2px rgb(0 0 0 / 0.05)',
      '--space-unit': '1rem',
    },
    attrs: {
      'data-layout': 'centered',
      'data-density': 'comfortable',
    },
  },
  {
    id: 'warm-editorial',
    label: 'Warm Editorial',
    description: 'Warm palette, tighter type',
    vars: {
      '--primary': '#c2410c',
      '--primary-hover': '#9a3412',
      '--surface': '#fffbf5',
      '--surface-muted': '#fef3e2',
      '--text-primary': '#431407',
      '--text-secondary': '#78716c',
      '--radius-sm': '0.25rem',
      '--radius-md': '0.375rem',
      '--radius-lg': '0.5rem',
      '--shadow-sm': '0 1px 3px rgb(67 20 7 / 0.08)',
      '--space-unit': '0.875rem',
      '--font-sans': '"Georgia", "Noto Serif JP", serif',
    },
    attrs: {
      'data-layout': 'centered',
      'data-density': 'compact',
    },
  },
  {
    id: 'cool-wide',
    label: 'Cool Wide',
    description: 'Cool palette, wide layout',
    vars: {
      '--primary': '#0891b2',
      '--primary-hover': '#0e7490',
      '--surface': '#f0fdfa',
      '--surface-muted': '#ecfeff',
      '--text-primary': '#134e4a',
      '--text-secondary': '#5eead4',
      '--radius-sm': '0.5rem',
      '--radius-md': '0.75rem',
      '--radius-lg': '1rem',
      '--shadow-sm': '0 4px 6px rgb(8 145 178 / 0.1)',
      '--space-unit': '1.125rem',
    },
    attrs: {
      'data-layout': 'wide',
      'data-density': 'comfortable',
    },
  },
];

export function getCandidateById(id: string): DesignCandidate | undefined {
  return DESIGN_CANDIDATES.find((c) => c.id === id);
}
