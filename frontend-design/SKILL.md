---
name: frontend-design
description: >-
  Design, build, or refactor application frontend UI with intentional visual
  direction, feature-oriented component architecture, and explicit page-flow
  boundaries. Use when creating or changing product screens, React/Next.js/Vue
  components, application layouts, design systems, forms, dashboards, or
  navigation flows; especially when deciding component placement, route versus
  modal behavior, or reusable UI boundaries. Do not use for a purely visual
  marketing/landing page when the existing design skill is a better match.
metadata:
  hermes:
    tags: [frontend, product-ui, ux, component-architecture, react, nextjs, accessibility]
    related_skills: [design, typography]
---

# Frontend Design

## Overview

Build product UI as a coherent system, not a page-sized mockup. Give every component one responsibility, keep domain state next to the feature that owns it, and make user-flow boundaries visible as routes or central dialogs.

Preserve an existing product's framework, design system, accessibility conventions, and repository rules unless the task explicitly changes them. Apply the structure below to new code and to touched areas; do not perform a speculative repository-wide migration.

## When to Use

Use this skill for:

- New or changed application screens, forms, dashboards, settings, and authenticated product UI
- Component placement, design-system work, feature extraction, or frontend refactoring
- Route, dialog, and navigation-flow design
- Reviewing whether a product UI has clear visual hierarchy and separable responsibilities

Do not use it as the primary guide for a campaign, portfolio, or landing page whose main problem is expressive visual art direction. Use the `design` skill for that case. Combine both when a product needs both an application architecture and a deliberately distinctive visual language.

## Delivery Workflow

1. **Inspect before changing.** Identify the framework, route convention, existing design system, path aliases, styling approach, and component boundaries. Reuse established conventions when they are sound.
2. **State the product decision.** Define the user, the page's one job, the feature boundary, the route/modal behavior after each task-starting action, and the responsive/a11y constraints.
3. **Make a compact design plan.** Choose content hierarchy, 4–6 color tokens, typography roles, spacing/radius/elevation rules, and the one visual choice specific to the product. Reject generic defaults that do not come from the brief.
4. **Place components before coding.** Classify each component using the four responsibility units below. Keep state, data adapters, and small child components with the feature that owns them.
5. **Implement the flow end to end.** Include loading, empty, error, disabled, focus, and mobile states. Do not leave a visual prototype with dead primary actions.
6. **Review the rendered result.** Check desktop and narrow viewports, keyboard navigation, contrast, focus visibility, dialog behavior, and whether the route/component boundaries remain intact.

When the task is unambiguous, execute this workflow without asking for routine approval. Surface a short plan before implementation only when design choices materially affect the result.

## Four Component Responsibility Units

Use these four units to decide placement and granularity. Adapt `src/` to the repository root; preserve an existing framework's route folder (`app/`, `pages/`, `routes/`, etc.).

| Unit | Location | Responsibility | Placement test | Examples |
| --- | --- | --- | --- | --- |
| **Primitive UI** | `src/components/ui/` | Present appearance and accessibility with no business knowledge | Could this be copied into another app and work without knowing its domain? | `Button`, `Dialog`, `Input`, `Badge`, `Skeleton` |
| **App Layout** | `src/components/layouts/` | Provide the app shell and navigation skeleton around route content | Does this wrap the page content area rather than represent a business task? | `AppHeader`, `SidebarNavigation`, `DashboardLayout` |
| **Feature Component** | `src/features/<feature>/components/` | Render and manipulate a bounded business concept | Does this depend on a domain type such as `User`, `Task`, or `Order`? | `TaskCard`, `AttendanceRow`, `JobStatusBadge` |
| **Page / Container** | `src/app/`, `src/pages/`, or route folder | Bind a URL to layout and feature composition | Is this the URL-addressable screen itself? | `tasks/page.tsx`, `routes/tasks.tsx` |

### Dependency Direction

Keep dependency direction narrow:

```text
route page / container
  ├─ app layout
  └─ feature public API
       └─ primitive UI
```

- Let **Primitive UI** depend only on presentation, accessibility utilities, and generic types. Never import domain models, feature hooks, API clients, or route code.
- Let **Layouts** own shell geometry and global navigation. Do not import a feature's private components or business state into a layout.
- Let **Features** own domain types, data adapters, feature hooks, interaction state, and their small private children. Import primitive UI, not route pages.
- Let **Pages** connect route params/search params, a layout, and public feature entry points. Keep page JSX intentionally thin: route metadata and composition are allowed; feature-specific DOM trees, page-local styling, and business interaction logic are not.
- Do not import another feature's internal file. Expose a deliberate public surface from `src/features/<feature>/index.ts` when cross-feature composition is genuinely required.
- Do not create a `components/common/` dumping ground. Promote a component to `components/ui/` only after it is truly domain-free. Otherwise keep it inside the owning feature or compose the features at the page level.
- Add import-boundary linting or path aliases when the project tooling supports it; do not introduce tooling solely for a tiny change.

### Feature Shape

Use the following as the default, not an inflexible template:

```text
src/
  components/
    ui/
      Button.tsx
      Dialog.tsx
    layouts/
      DashboardLayout.tsx
  features/
    tasks/
      api/
        tasks.ts
      components/
        TaskCard.tsx
        TaskList.tsx
        TaskEditorDialog.tsx
      hooks/
        useTaskFilters.ts
      types.ts
      index.ts
  app/
    tasks/
      page.tsx
```

Keep state colocated with the lowest common owner that needs it. A child used only by `TaskList` belongs in the `tasks` feature, even if it looks small enough to be reusable. Export only the feature components/types another route actually needs through `index.ts`.

## Page and Interaction Boundaries

### One Page, One Feature

Treat each URL screen as one coherent user job. A page may compose subcomponents and supporting data, but it must have a single primary feature/purpose that a user can name. If a screen has two independently actionable workflows, split them into routes or make one an explicitly invoked dialog flow.

A dashboard can be a feature when its purpose is one coherent overview. Do not use this rule to scatter every card into an arbitrary separate URL.

### Actions Must Change Context Clearly

For any action that opens a form, detail workspace, configuration flow, or other screen-sized task:

- Navigate to a dedicated route **or** open a **central modal dialog**.
- Do **not** reveal that task inline below the triggering button, accordion, or card while leaving the origin page visually active.
- In the dialog case, use a viewport-centered modal with a backdrop that makes the origin page recede. Trap focus, label the dialog, support Escape when it is safe, prevent background interaction, and restore focus to the trigger on close.
- Prefer a route for multi-step work, substantial editing, shareable/deep-linkable states, or flows that need browser history. Prefer a dialog only for short, bounded work that completes and returns to the same context.
- Local controls that do not create a new screen—toggle, sort, filter, select, inline status change—may update in place. Do not misclassify a full form or detail flow as a local control.

After completion, use direct feedback that matches the action vocabulary: `Save changes` → `Changes saved`; `Publish` → `Published`. Keep action labels specific about their outcome.

### Footer Rule

Include the app footer on every page by default. Omit it only from the **main map-view page**, where persistent map interaction is the primary experience. An embedded map, map preview, or secondary map section does not qualify for this exception.

## Visual Direction for Product UI

Ground visual choices in the product's actual subject matter, audience, and primary task. Do not attach the same palette, hero composition, rounded-card grid, shadows, gradients, or type treatment to every project.

Before implementation, write a compact decision record when the task needs visual design:

```text
Product / user / job:
Visual premise:
Tokens: surface, ink, muted, accent, critical, success
Type roles: display, UI/body, numeric/technical (if needed)
Layout: alignment, density, reading measure, breakpoint behavior
Distinctive choice: one detail that comes from this product—not a generic trend
```

Apply these principles:

- Make typography carry hierarchy. Set deliberate scale, weight, line-height, and readable line lengths rather than using type as neutral filler.
- Use color, borders, elevation, and spacing to encode information hierarchy. Decoration must serve a content or interaction purpose.
- Spend boldness once. Make one product-relevant element memorable and keep surrounding UI disciplined.
- Use motion to explain a user-caused state change. Respect reduced-motion preferences; avoid scattered entrance animations and generic hover effects.
- Use existing tokens and components before inventing new values. If a token layer does not exist, introduce a small semantic token system instead of scattering one-off literals.
- Do not use uppercase labels, gratuitous eyebrow text, decorative numbering, arrows appended to every CTA, or a highlighted word in every heading unless the content genuinely needs that treatment.
- Do not use identical rounded cards as the default answer to every information group. Vary structure only when it improves meaning and scanability.

## Content and State Design

Write interface text for the person using the product, not for the implementation.

- Name concepts with familiar nouns and plain active verbs. Keep the same term through trigger, dialog/page, confirmation, and error message.
- Make primary CTAs describe the result: `Create task`, `Save changes`, `Invite member`. Avoid vague verbs such as `Submit` when a precise verb exists.
- Treat empty states as an instruction to take the next useful action. Treat errors as a precise explanation plus recovery path, never an apology or a vague failure.
- Design normal, loading, empty, error, disabled, and success states before declaring a feature complete. Handle optimistic updates and destructive actions according to the product's existing conventions.

## Quality Floor

Meet these constraints regardless of visual direction:

- Use semantic controls; provide visible keyboard focus and logical tab order.
- Associate labels, descriptions, and errors with their controls. Do not rely on color alone for meaning.
- Make dialogs accessible: correct dialog semantics, initial focus, focus containment, close behavior, and no interactive background.
- Keep touch targets usable and layouts readable at narrow widths. Test at least one desktop and one mobile/narrow viewport.
- Maintain sufficient contrast and respect `prefers-reduced-motion`.
- Do not introduce raw interactive `div`s, missing image alt text, or keyboard-inaccessible custom controls when semantic elements solve the problem.

## Verification Checklist

Before finishing, verify all applicable items:

### Architecture

- [ ] Every changed component is placed by its responsibility rather than convenience.
- [ ] Primitive UI contains no domain/API/feature imports.
- [ ] Feature internals remain private; cross-feature use goes through an intentional public API.
- [ ] Route pages are composition layers, not large feature implementations.
- [ ] New state lives with its owning feature.

### Flow

- [ ] The page has one primary user job.
- [ ] Screen-sized follow-up actions navigate or open a central accessible modal; none expand inline beneath the trigger.
- [ ] Multi-step or deep-linkable work uses a route.
- [ ] Footer is present unless the screen is the main map view.

### Design and quality

- [ ] Visual choices derive from the product rather than an AI-default look.
- [ ] Typography, spacing, and tokens establish clear hierarchy.
- [ ] Normal, loading, empty, error, disabled, and success states are handled where relevant.
- [ ] Keyboard, focus, contrast, responsive layout, and reduced motion have been checked.
- [ ] Rendered screenshots or live previews have been inspected when the environment supports them.

## Completion Report

When delivering frontend work, report only the decisions that affect future changes:

- The route and feature boundary added or changed
- New/changed public component APIs and where they live
- Whether the action uses a route or central dialog, and why
- Validation performed and known limitations
