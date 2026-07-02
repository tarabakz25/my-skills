# Design Review Checklist

## Legend

- **[Critical]** → Must fix (UX breakdown or accessibility violation)
- **[Warning]** → Recommended fix (consistency gap or improvement opportunity)
- **[Suggestion]** → Optional improvement

---

## 1. Accessibility (WCAG 2.1 AA)

### Color Contrast
- [ ] **[Critical]** Body text (under 16px): contrast ratio **4.5:1 or higher**
- [ ] **[Critical]** Large text (18px+ or 14px bold): contrast ratio **3:1 or higher**
- [ ] **[Critical]** UI component borders and icons: contrast ratio **3:1 or higher**
- [ ] **[Warning]** Decorative-only elements do not need contrast (add `aria-hidden="true"`)

### Keyboard Operation
- [ ] **[Critical]** All interactive elements are focusable via Tab
- [ ] **[Critical]** Focus ring (`focus-visible:ring-*`) is visible
- [ ] **[Critical]** Not using `div/span` with onClick (use `button` / `a`)
- [ ] **[Critical]** Modals/dropdowns implement focus trap
- [ ] **[Warning]** Logical Tab order (DOM order matches visual order)

### Semantics and ARIA Labels
- [ ] **[Critical]** Inputs have matching `<label>` or `aria-label`
- [ ] **[Critical]** Icon-only buttons have `aria-label`
- [ ] **[Critical]** Meaningful images have `alt` text (decorative images use `alt=""`)
- [ ] **[Critical]** Heading hierarchy is correct (H1 > H2 > H3, no skipped levels)
- [ ] **[Warning]** Landmark elements are used (`<main>`, `<nav>`, `<header>`, `<footer>`)
- [ ] **[Warning]** Error messages use `role="alert"` or `aria-live="polite"`
- [ ] **[Warning]** Loading states use `aria-busy="true"` or `role="status"`

---

## 2. Responsive Design

### Breakpoints
- [ ] **[Critical]** No horizontal scroll at 375px (iPhone SE)
- [ ] **[Critical]** Tap targets are at least **44×44px**
- [ ] **[Warning]** Text wraps and remains readable at 320px
- [ ] **[Warning]** `sm:` `md:` `lg:` are applied mobile-first

### Layout
- [ ] **[Warning]** Images/media have `max-w-full` or `object-fit`
- [ ] **[Warning]** Not using fixed widths (`w-[500px]`) — prefer `max-w-*` or `w-full`
- [ ] **[Suggestion]** Single column on mobile, multi-column on desktop

---

## 3. Design System Consistency

### Color and Typography
- [ ] **[Warning]** Not using arbitrary values outside tokens (`text-[#333]`, `bg-[#fff]`)
- [ ] **[Warning]** Not using arbitrary font sizes (`text-[13px]`)
- [ ] **[Warning]** Text colors match purpose (e.g., supporting text uses `text-neutral-600`)

### Spacing and Components
- [ ] **[Warning]** `padding/margin` follow the spacing scale (4px base)
- [ ] **[Warning]** Repeated patterns are reused as components, not copy-pasted
- [ ] **[Suggestion]** `rounded` and `shadow` match component type

---

## 4. Interaction and States

- [ ] **[Critical]** Interactive elements have hover/focus/active states
- [ ] **[Critical]** Disabled elements have `disabled` attribute and visual treatment
- [ ] **[Warning]** Form validation errors appear inline (real-time preferred, not only after submit)
- [ ] **[Warning]** Loading indicator during async operations
- [ ] **[Warning]** Destructive actions (delete, etc.) have confirmation dialog
- [ ] **[Suggestion]** Cursor is appropriate on hover (buttons: `cursor-pointer`, disabled: `cursor-not-allowed`)

---

## 5. Performance

- [ ] **[Warning]** Not overusing `transition-all` (limit to properties that change)
- [ ] **[Warning]** `useEffect` + state updates are not causing render loops
- [ ] **[Warning]** Large lists use virtualization (`react-window`, `tanstack-virtual`)
- [ ] **[Suggestion]** Images have `loading="lazy"` and appropriate `width/height`
- [ ] **[Suggestion]** Animated elements use `will-change: transform` or `transform: translateZ(0)`

---

## 6. General UX (Nielsen's Heuristics)

- [ ] **[Critical]** Current location and state are visible (active nav, progress indicators)
- [ ] **[Critical]** Errors use user-friendly language with cause and fix
- [ ] **[Warning]** Undo and cancel are available where appropriate
- [ ] **[Warning]** Irreversible actions cannot run without confirmation
- [ ] **[Suggestion]** Defaults and autocomplete reduce cognitive load

---

## Review Output Format

```markdown
## Design Review Results

### [Critical] Required Fixes (N items)
- **Accessibility**: Using `<div onClick>` instead of `<button>`
  → Change to `<button>` and add `focus-visible:ring-*`

### [Warning] Recommended Fixes (N items)
- **Design system**: Using `text-[13px]`
  → Change to `text-xs` (12px) or `text-sm` (14px)

### [Suggestion] Optional Improvements (N items)
- **UX**: Adding a confirmation dialog after delete would prevent accidental actions
```
