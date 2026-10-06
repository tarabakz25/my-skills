---
name: typography
description: >-
  Choose and implement distinctive font pairings (display/body/mono), type scales,
  and font loading for web UI via Google Fonts or Adobe Fonts. Use when the user
  asks for /typography, font pairing, type hierarchy, or font loading; or whenever
  the design skill (/design) is invoked and type choices are not yet locked.
disable-model-invocation: true
metadata:
  hermes:
    tags: [typography, fonts, google-fonts, adobe-fonts, design, css, frontend]
    related_skills: [design, web-perf]
---

# Typography

## Overview

Lock a intentional type system before styling UI: pairing → scale → loading → CSS. Prefer Google Fonts or Adobe Fonts. Do not default to Inter, Roboto, Arial, system-ui, or "safe" generic stacks unless the brief explicitly asks for neutral product UI.

## When to Use

- User says `/typography`, asks for font pairing, type scale, or font loading
- `/design` (or the design skill) is active and fonts are not yet committed
- Building landing/marketing HTML where type carries brand voice

**Do not use when:**
- An existing brand kit or design system already owns fonts
- The task is only color, layout, or motion with fonts already locked

## Decision Flow

Copy and complete before coding:

```
Type Lock:
- [ ] 1. Tone locked
- [ ] 2. Roles assigned (display / body / mono?)
- [ ] 3. Contrast strategy chosen
- [ ] 4. 2–3 candidate pairings proposed
- [ ] 5. One pairing locked + reject reasons noted
- [ ] 6. Scale + measure locked
- [ ] 7. Source + loading strategy locked (Google | Adobe)
```

### 1. Tone

Pick one primary voice (extreme is fine; muddled midtones are not):

| Tone | Type tendency |
|------|----------------|
| Editorial / magazine | High-contrast serif display + quiet sans body |
| Luxury / heritage | Refined serif or didone display; restrained body |
| Tech / product | Geometric or neo-grotesk; optional mono accent |
| Playful / toy | Rounded display or soft slab; friendly sans body |
| Brutalist / raw | Grotesk, mono, or system-adjacent with intentional roughness |
| Retro / archival | Historical display + period-appropriate body |
| Organic / human | Soft serif or humanist sans; avoid cold geometrics |

Write one sentence: *“Typography should feel ___ because ___.”*

### 2. Roles

Assign fonts to roles (usually 2; add mono only if code, data, or labels need it):

| Role | Job | Typical face |
|------|-----|--------------|
| **Display** | Hero, H1–H2, pull quotes | Distinctive; carries voice |
| **Body** | Paragraphs, UI chrome, long read | High readability at 16–18px |
| **Mono** (optional) | Code, captions, meta, prices | Clear at small sizes |

One family for everything is allowed only when the face has strong optical sizes/weights and the tone is intentionally monofamily.

### 3. Contrast Strategy

Pair by **difference**, not by similarity:

| Strategy | Rule | Example shape |
|----------|------|----------------|
| Serif × Sans | Classic editorial contrast | Display serif + body sans |
| Display × Text | Same genre, different texture | Expressive sans + neutral sans |
| Soft × Hard | Mood vs structure | Rounded display + crisp grotesque |
| Mono accent | Voice + utility | Display/body pair + mono for meta |

**Avoid:** two similar neo-grotesks; two soft rounded faces; matching “friendly” fonts that blur hierarchy.

Check: at a glance, can you tell which face is the star?

### 4. Propose 2–3 Pairings

For each candidate, state:

```
Pair N:
  Display: <Family> (<weights>)
  Body:    <Family> (<weights>)
  Mono:    <Family or —>
  Source:  Google Fonts | Adobe Fonts
  Why:     <one line tied to Tone>
  Risk:    <legibility / licensing / weight gaps>
```

Prefer faces available on **Google Fonts** or **Adobe Fonts**. Verify the exact family name and available weights on the vendor before locking.

For **Adobe Fonts**, verify with `ADOBE_API_KEY` (see [Adobe Fonts API](#adobe-fonts-api)) — do not guess availability from memory.

Banned defaults unless the user insists: Inter, Roboto, Open Sans, Lato, Montserrat, Arial, Helvetica, system-ui-only stacks.

### 5. Lock One

Choose one pairing. Briefly say why the others lost (too safe, weak contrast, wrong era, poor JP coverage if needed, missing italic/weight, etc.).

Announce the lock in chat before writing CSS:

```
Locked type:
  Display: …
  Body: …
  Mono: …
  Source: Google Fonts | Adobe Fonts
  Scale: … (see below)
```

### 6. Scale + Measure

Define a small scale (do not invent a 12-step system unless needed):

| Token | Use | Starting point |
|-------|-----|----------------|
| `--text-xs` | Meta, labels | 0.75–0.8125rem |
| `--text-sm` | Secondary UI | 0.875rem |
| `--text-base` | Body | 1–1.125rem |
| `--text-lg` | Lead / H3 | 1.25–1.5rem |
| `--text-xl` | H2 | 1.75–2.25rem |
| `--text-display` | Hero / H1 | 2.75–4.5rem+ (clamp) |

Rules:

- Body line-height ≈ **1.5–1.7**; display ≈ **1.05–1.2**
- Body measure ≈ **45–75ch** for long prose
- Prefer `clamp()` for display sizes on fluid layouts
- Limit loaded weights (e.g. display 600/700; body 400/500/700) — do not load the whole family

### 7. Source + Loading

#### Google Fonts

Prefer **self-host** or official CSS API with subsetting. Minimal pattern:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=DISPLAY:wght@600;700&family=BODY:wght@400;500;700&display=swap"
  rel="stylesheet"
/>
```

- Use `display=swap` (or optional + `size-adjust` / `ascent-override` if CLS matters)
- Request only needed weights/styles
- For Latin-only UI, keep default subsets; add `text=` or unicode-range subsetting when bundle size matters

#### Adobe Fonts (Typekit)

Requires `ADOBE_API_KEY` in the environment (Typekit user token). Never print, log, or commit the key.

1. Verify candidates via API (slug → name, variations, libraries)
2. Create/use a Web Project (kit) that includes the locked families
3. Read exact `css_names` from the kit endpoint; embed:

```html
<link rel="stylesheet" href="https://use.typekit.net/KIT_ID.css" />
```

4. Use those `css_names` in `font-family` — kit CSS is source of truth
5. Keep the kit lean (few families / few variations)

##### Adobe Fonts API

Auth header: `X-Typekit-Token: $ADOBE_API_KEY`  
Base: `https://typekit.com/api/v1/json`  
Docs: https://fonts.adobe.com/docs/api

Helper (preferred):

```bash
python3 ~/.skills/typography/scripts/adobe_fonts.py ping
python3 ~/.skills/typography/scripts/adobe_fonts.py family source-serif-4
python3 ~/.skills/typography/scripts/adobe_fonts.py kits
python3 ~/.skills/typography/scripts/adobe_fonts.py kit KIT_ID
```

If the helper is unavailable, equivalent curls (token stays in the header — do not echo it):

```bash
# Confirm auth + list kits
curl -sS -H "X-Typekit-Token: $ADOBE_API_KEY" \
  https://typekit.com/api/v1/json/kits

# Family by slug (follows redirect to id)
curl -sS -L -H "X-Typekit-Token: $ADOBE_API_KEY" \
  https://typekit.com/api/v1/json/families/SOURCE-SERIF-4-SLUG

# Kit detail → css_names + variations for CSS
curl -sS -H "X-Typekit-Token: $ADOBE_API_KEY" \
  https://typekit.com/api/v1/json/kits/KIT_ID
```

Variation codes use FVD (e.g. `n4` = regular, `n7` = bold, `i4` = italic). Only include variations the design uses.

#### Shared CSS tokens

```css
:root {
  --font-display: "Display Family", serif;
  --font-body: "Body Family", sans-serif;
  --font-mono: "Mono Family", ui-monospace, monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1.0625rem;
  --text-lg: 1.375rem;
  --text-xl: 2rem;
  --text-display: clamp(2.75rem, 6vw, 4.5rem);

  --leading-body: 1.6;
  --leading-display: 1.1;
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-body);
}

h1, .display {
  font-family: var(--font-display);
  font-size: var(--text-display);
  line-height: var(--leading-display);
  font-weight: 700;
}
```

Fallbacks: generic `serif` / `sans-serif` / `monospace` only — never silently fall back to Inter.

## Output Contract

When this skill runs, always produce:

1. Completed **Type Lock** checklist (or state what’s still open)
2. The locked pairing (families, weights, source)
3. Scale tokens (or equivalent)
4. Embed snippet (Google link or Adobe kit) + CSS variables
5. One-line risk note (FOIT/FOUT, weight gaps, licensing)

Do not start visual CSS for a new aesthetic until step 5 (pairing lock) is done — unless fonts are inherited from a brand system.

## With `/design`

When the design skill is active:

1. Read this skill and run the Decision Flow during Design Thinking
2. Put the type lock next to Purpose / Tone / Differentiation
3. Then implement color, motion, and layout using the locked faces

## Common Pitfalls

- Pairing two similar sans faces → hierarchy collapses
- Loading 8+ weights → slow LCP / layout shift
- Choosing fonts from memory without checking Google/Adobe availability
- Oversized display with tight leading and long headlines → overflow
- Using Inter/Roboto “just for body” after a distinctive display → kills the voice
- Adobe kit family names guessed wrong → silent fallback to generic
- Using Adobe without `ADOBE_API_KEY` / skipping API verify → wrong slug or missing weights
- Leaking `ADOBE_API_KEY` into chat, commits, or HTML

## Verification Checklist

- [ ] Tone sentence written
- [ ] Display/body(/mono) roles assigned with contrast strategy
- [ ] Exactly one pairing locked; rejects explained
- [ ] Families verified on Google Fonts or Adobe Fonts API
- [ ] If Adobe: `adobe_fonts.py family` (or kit) run; `css_names` used in CSS
- [ ] Weights / variations limited to what’s used
- [ ] Scale + line-height + measure set
- [ ] preconnect + embed (Google) or kit CSS (Adobe) present
- [ ] CSS variables wired; no banned default fonts unless requested
- [ ] Short risk note recorded
- [ ] `ADOBE_API_KEY` never printed or committed
