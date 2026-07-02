---
name: ui-ux-designer
description: "Use when designing, implementing, or reviewing web/mobile UI with Tailwind CSS + React/Next.js. Covers persona-driven IA, style guides, design tokens, component patterns, a11y (WCAG 2.1 AA), responsive layout, and self-review checklists."
version: 2.1.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ui, ux, design, tailwind, react, accessibility]
    related_skills: [frontend-design, design-system, accessibility, browser-qa, design-tweaks-ui]
---

# UI/UX Designer

## Overview

Design, implement, and review frontend UI for web and mobile apps from **both user and developer perspectives**.

Uses Tailwind CSS + React/Next.js as the primary stack and defines a workflow from persona → sitemap → style guide → component implementation → self-review. Detailed principles, patterns, and checklists live in `references/`; SKILL.md focuses on decision criteria and procedures.

**Core philosophy**: Beautiful, usable, and easy to implement. Function over decoration; reduce confusion over chasing novelty.

**Priority order**:
1. Usability (operability and clarity)
2. Accessibility (WCAG 2.1 AA compliance)
3. Design consistency (design system alignment)
4. Responsive design (mobile-first)
5. Performance (minimal re-renders, efficient CSS)

UI design fundamentals (14 principles) → [`references/ui-principles.md`](references/ui-principles.md)

## When to Use

**Use this skill when:**
- Creating or designing new UI
- Adjusting or improving existing UI
- Adding a dev-only tweaks popup to compare design candidates via buttons → also use `design-tweaks-ui`
- Requesting design review or feedback
- Implementing components, screen layouts, or design systems
- Evaluating UI for accessibility, responsiveness, or performance

**Don't use for:**
- **Visual direction exploration only** (strong aesthetic is the main goal) → prefer `frontend-design`
- **Full codebase design system audit or token generation** → prefer `design-system`
- **Deep WCAG 2.2 a11y audit or ARIA specifications** → prefer `accessibility`
- **E2E UI behavior verification** → prefer `browser-qa`
- Backend API design or infrastructure (no UI involvement)

## Workflow

### New Design Creation

1. **Requirements**: Understand screen purpose, target users, and primary actions
2. **Personas (1–2)**: Define user attributes, goals, pain points, and usage context → [`references/style-guide.md`](references/style-guide.md)
3. **Sitemap**: Visualize screen structure with Mermaid; confirm main flows are reachable within 3 clicks → [`references/style-guide.md#sitemap-template`](references/style-guide.md)
4. **Style guide**: Define colors, typography, and component styles with project-specific values → [`references/style-guide.md#style-guide-output-template`](references/style-guide.md)
5. **Information architecture**: Set content priority and layout structure (based on personas and sitemap)
6. **Component selection**: Pick from existing patterns → [`references/component-patterns.md`](references/component-patterns.md)
7. **Design tokens**: Apply style guide tokens; prefer existing project tokens when present → [`references/design-tokens.md`](references/design-tokens.md)
8. **Implementation**: Code with Tailwind + React
9. **Self-review**: Verify quality with the checklist → [`references/review-checklist.md`](references/review-checklist.md)

### Design Adjustments

1. Read existing code and understand intent before changing anything
2. Do not use values outside design tokens (magic numbers)
3. Check impact of a single component change on other areas
4. Re-verify critical items in [`references/review-checklist.md`](references/review-checklist.md) after adjustments

### Design Review

Use [`references/review-checklist.md`](references/review-checklist.md) and list findings by category:

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | UX breakdown or accessibility violation | Must fix |
| **Warning** | Consistency gaps or room for improvement | Recommended fix |
| **Suggestion** | Optional improvement | Optional |

See the output format at the end of the same file.

## Tech Stack

| Category | Technology |
|----------|------------|
| Primary | Tailwind CSS v3+, React 18+, Next.js App Router |
| Supporting | shadcn/ui, Radix UI, Framer Motion |

### Tailwind Rules

```tsx
// Good: classes aligned with design tokens
<button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">

// Bad: magic numbers and arbitrary values
<button className="bg-[#1a73e8] text-[13px] px-[14px]">
```

- Use arbitrary values `[]` only when existing tokens cannot cover the need
- Consider `@apply` when the same pattern repeats 3+ times
- Dark mode: combine `dark:` variants with semantic colors

## References

| File | Content | When to Read |
|------|---------|--------------|
| [`references/ui-principles.md`](references/ui-principles.md) | 14 UI design principles + review questions | Design decisions and reviews |
| [`references/style-guide.md`](references/style-guide.md) | Persona, sitemap, and style guide templates | Early phase of new work |
| [`references/design-tokens.md`](references/design-tokens.md) | Default color, type, spacing system | Implementation start, token checks |
| [`references/component-patterns.md`](references/component-patterns.md) | Button/Form/Card/Nav implementation patterns | Component selection and coding |
| [`references/review-checklist.md`](references/review-checklist.md) | a11y, responsive, design system, performance | Reviews and post-implementation |

## Common Pitfalls

1. **Skipping personas and sitemap before coding** — IA breaks later. Do not skip steps 2–4 on new work.

2. **Confusing this skill with frontend-design** — This skill focuses on UX principles, tokens, and a11y alignment. Use `frontend-design` when a strong aesthetic direction is needed.

3. **Tailwind arbitrary values as magic numbers** — `text-[13px]` or `bg-[#333]` break the design system. Use tokens or scales from `design-tokens.md`.

4. **Building buttons with `div` + `onClick`** — Fails keyboard and screen reader support. Use `<button>` or Radix primitives from [`references/component-patterns.md`](references/component-patterns.md).

5. **Returning only "suggestions" in reviews** — List critical and warning items first with file paths and concrete fixes. Follow the output format in [`references/review-checklist.md`](references/review-checklist.md).

6. **Ignoring existing project tokens** — `design-tokens.md` is the default. Prefer `tailwind.config` or CSS variables in the repo when they exist.

7. **Forgetting mobile-first** — Desktop-first layouts with only `max-w-*` break at 375px. Apply `sm:` `md:` `lg:` from small to large.

## Verification Checklist

After implementation or review:

- [ ] Persona main flow is achievable within 3 clicks (new work)
- [ ] No arbitrary values outside design tokens remain
- [ ] All **Critical** items in [`references/review-checklist.md`](references/review-checklist.md) pass
- [ ] No horizontal scroll at 375px width
- [ ] Interactive elements have hover / focus / disabled states
- [ ] Form errors, loading, and destructive actions have appropriate feedback
- [ ] Changed components have no unintended side effects elsewhere

### Frontmatter Validation (on skill updates)

```bash
python3 -c "
import yaml, re, pathlib
p = pathlib.Path('~/.skills/ui-ux-designer/SKILL.md').expanduser()
content = p.read_text()
assert content.startswith('---'), 'Must start with ---'
m = re.search(r'\n---\s*\n', content[3:])
fm = yaml.safe_load(content[3:m.start()+3])
assert fm['name'] == 'ui-ux-designer'
assert len(fm['description']) <= 1024
assert len(content) <= 100_000
print('OK:', fm['version'])
"
```
