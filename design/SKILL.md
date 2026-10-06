---
name: design
description: >-
  Create distinctive, high-craft frontend HTML/CSS with bold aesthetic direction,
  intentional typography, color, motion, spatial composition, and CSS variables
  instead of magic numbers. Use when building UI that is not constrained by an
  existing brand or design system; when the goal is memorable, creative visual HTML
  rather than token-aligned product UI; when avoiding CSS magic numbers or defining
  design tokens as custom properties; or when the user asks for /design, aesthetic
  direction, or uniquely styled landing/marketing pages.
disable-model-invocation: true
metadata:
  hermes:
    tags: [design, frontend, html, css, typography, aesthetic, ui, creative]
    related_skills: [typography, aside-browser, web-perf]
---

# Design

## Overview

Build distinctive frontend HTML with aesthetic detail and creative judgment when no existing brand or design system owns the look.

Commit to a visual direction before coding. Match implementation complexity to the aesthetic vision.

## When to Use

Use when creating frontend UI that is not dominated by an existing brand or design system, and the goal is highly original HTML with aesthetic detail and creative judgment.

**Do not use when:**
- The work must follow an existing brand or design system
- The task is product UX process, design tokens, or a11y review alone
- The task is a dev-only candidate comparison panel

## 1. Design Thinking (Before Coding)

Commit to a bold aesthetic direction.

**Purpose**: Whose problem does this UI solve?

**Tone**: Choose an extreme — stark minimal, maximalism, retro-futurism, organic, luxury, playful/toy-like, editorial/magazine, brutalist, art deco/geometric, pastel, industrial, etc.

**Differentiation**: What makes it unforgettable? What is the one memorable detail?

**Typography**: Before coding, load and follow `typography` (`~/.skills/typography/SKILL.md`). Run its Decision Flow and lock display/body(/mono), scale, and Google Fonts or Adobe Fonts loading. Do not proceed with visual CSS until the type lock is announced.

Intentionality beats intensity. Bold maximalism and refined minimalism both work when deliberate.

## 2. Aesthetic Guidelines

**Typography**: Follow the `typography` skill. Avoid generic fonts (Arial, Inter, Roboto, system). Pair a distinctive display face with a refined body face; implement via Google Fonts or Adobe Fonts with limited weights.

**Color & Theme**: Commit to one aesthetic. Unify with CSS variables. Prefer a dominant color + sharp accent over evenly distributed neutrals.

**No magic numbers**: Do not hardcode spacing, sizing, color, radius, shadow, or duration literals in rules. Define them once as CSS custom properties on `:root` (or the project's token layer) and reference those variables. Escape hatch: a one-off experiment value, or a value already owned by an existing design system's tokens.

**Motion**: Animate effects and micro-interactions. Prefer CSS-only in HTML. One staged page-load reveal usually beats scattered flourishes.

**Spatial Composition**: Unexpected layouts, asymmetry, overlap, diagonal flow, elements that break the grid, bold whitespace or controlled density.

**Backgrounds & Details**: Avoid flat single-color fills. Build atmosphere — gradient meshes, noise, geometric patterns, layered transparency, dramatic shadows, decorative borders, grain overlays.

Vary light/dark, type, and aesthetic every generation; do not converge on the same choices. Match implementation complexity to the vision (crafted spectacle for maximalism; restraint and precision for minimalism).

## Common Pitfalls

- Generic fonts or evenly muted palettes → pretty but forgettable
- Coding components before locking Purpose / Tone / Differentiation
- Converging on the same AI defaults every run (dark purple gradients, cream + serif, broadsheet, etc.)
- Maximal effects on a minimal brief, or flat fills on a maximal brief
- Scattered magic numbers (`padding: 23px`, `color: #3a7`, `transition: 0.37s`) instead of shared CSS variables
- Overriding an existing design system with this skill

## Verification Checklist

- [ ] Stated Purpose / Tone / Differentiation before coding
- [ ] Distinctive type pairing locked via `typography` skill (no generic UI fonts)
- [ ] CSS variables; dominant color + accent
- [ ] No magic numbers — spacing/size/color/radius/shadow/duration via variables
- [ ] Depth in backgrounds, or intentional flat restraint
- [ ] CSS-first motion with at least one intentional moment
- [ ] Spatial judgment (asymmetry, overlap, whitespace, or density)
- [ ] Avoided default AI looks / prior-run convergence
- [ ] Complexity matches Tone
