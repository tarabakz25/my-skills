---
name: slidev
description: Create, edit, analyze, and refactor Slidev presentations. Use when working with Slidev projects, slides.md files, or when users mention presentations, slides, or Slidev. Supports slide creation, structure analysis, and refactoring operations.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Slidev - Presentation Development Assistant

This skill helps you work with Slidev, a web-based presentation tool for developers that uses Markdown and Vue.js.

## What is Slidev?

Slidev is a presentation slides maker for developers that lets you:
- Write slides in Markdown format
- Use Vue components and custom styling
- Include code snippets with syntax highlighting
- Add diagrams (Mermaid), math (KaTeX), and animations
- Interactive features (drawing, recording, remote access)
- Version control your presentations with Git
- Export to PDF, PPTX, PNG, or SPA

## Core Capabilities

### 1. Slide Creation & Editing

**Initialize New Project**
```bash
npm init slidev@latest
# or
pnpm create slidev
```

**Add New Slides**
- Slides are separated by `---` with blank lines
- Each slide can have optional frontmatter (YAML between `---`)
- First slide's frontmatter is the "headmatter" (global config)

**Slide Structure**
```markdown
---
# Headmatter (first slide only)
theme: seriph
title: My Presentation
background: /cover.jpg
---

# First Slide
Content here

---
layout: center
background: /slide2.jpg
---

# Second Slide
Content here
```

### 2. Structure Analysis

**Analyze slides.md:**
- Parse all slides and their frontmatter
- List slide titles and layouts
- Count total slides
- Identify used layouts and themes
- Find slides with specific properties

**Example Analysis Output:**
```
Slide 1: Cover (layout: cover)
Slide 2: Introduction (layout: center)
Slide 3: Code Demo (layout: default)
...
Total: 25 slides
Layouts used: cover, center, default, two-cols, image-right
```

### 3. Refactoring Support

**Slide Reordering**
- Move slides to different positions
- Group related slides together
- Reorganize presentation flow

**Frontmatter Standardization**
- Ensure consistent frontmatter across slides
- Add missing properties
- Remove unused properties
- Update layout choices

**Layout Optimization**
- Suggest appropriate layouts for content
- Convert between layouts
- Add responsive design considerations

### 4. Theme & Addon Management

**Install Themes**
- Specify theme in headmatter frontmatter
- Automatic installation prompts when theme not found
- Use abbreviated names for official themes (e.g., `seriph` instead of `slidev-theme-seriph`)
- Browse Theme Gallery: https://sli.dev/resources/theme-gallery

**Install Addons**
- Add multiple addons in headmatter
- Supports official and community addons
- Browse Addon Gallery: https://sli.dev/resources/addon-gallery

**Example Configuration:**
```yaml
---
theme: seriph              # Single theme (auto-install prompt)
addons:                    # Multiple addons allowed
  - excalidraw
  - '@slidev/plugin-notes'
---
```

**Theme vs Addons:**
- Themes: One per project, comprehensive styling
- Addons: Multiple allowed, specific features

## Common Workflows

### Workflow 1: Create New Presentation

1. Initialize project: `npm init slidev@latest`
2. Navigate to project directory
3. Edit `slides.md` with slide content
4. Run dev server: `npm run dev`
5. Preview at http://localhost:3030

### Workflow 2: Edit Existing Slides

1. Read current `slides.md`
2. Analyze structure and content
3. Make requested edits using Edit tool
4. Verify changes maintain valid Markdown

### Workflow 3: Refactor Presentation

1. Read and parse `slides.md`
2. Analyze current structure
3. Propose refactoring plan
4. Apply changes (reorder, update frontmatter, optimize layouts)
5. Verify slide separators and frontmatter syntax

### Workflow 4: Add Code Slides

1. Identify insertion point
2. Add new slide with appropriate layout
3. Include code blocks with language tags
4. Optional: Add line highlighting or animations

Example: Add a slide with a TypeScript function that includes syntax highlighting and line number highlighting on specific lines (2, 4-6)

### Workflow 5: Use Interactive Features

1. **Enable Drawing/Annotations:**
   - Configure in headmatter: `drawings: { enabled: true }`
   - Use Drauu library for real-time annotations
   - Toggle drawing mode during presentation

2. **Recording & Camera:**
   - Set `record: dev` in headmatter
   - Click record button in navigation UI
   - Optionally enable camera view overlay

3. **Remote Access:**
   - Enable `remote: true` in headmatter
   - Share presentation URL for audience access
   - Supports Cloudflare Quick Tunnels

4. **Draggable Elements:**
   - Use `<VDrag>` and `<VDragArrow>` components
   - Position elements interactively during presentation

## Key Slidev Features to Leverage

### Layouts
- `cover`: Title slide
- `center`: Centered content
- `default`: Standard slide with title
- `two-cols`: Two-column layout
- `image-right`, `image-left`: Content with side image
- `quote`: For quotations
- `section`: Section divider
- Custom layouts from themes

### Frontmatter Options
```yaml
---
layout: default           # Layout to use
background: /img.jpg     # Background image or color
class: text-center       # CSS classes
clicks: 3                # Click steps for animations
transition: fade         # Slide transition effect
hideInToc: true          # Hide from table of contents
---
```

### Code Features
- Syntax highlighting with Shiki
- Line highlighting: `{1,4-6}`
- Line numbers: use language with `{1|3|all}`
- Monaco editor for live coding
- Shiki Magic Move for smooth code transitions
- TwoSlash integration for type hints
- Code execution support
- Multiple code snippets per slide

### Interactive Components
- `<VDrag>` - Draggable elements
- `<VDragArrow>` - Draggable arrows
- `<VClick>`, `<VClicks>` - Click-based animations
- `<VSwitch>` - Toggle between content on clicks
- Rough Notation for highlighted text effects
- `<SlidevVideo>` - Video with playback controls

### Diagrams & Math
- Use Mermaid for diagrams (flowcharts, sequence diagrams, etc.)
- Inline math with single dollar signs: E = mc^2
- Block math with double dollar signs for complex equations
- LaTeX syntax supported via KaTeX

## Best Practices

1. **Consistent Structure**
   - Use headmatter for global settings
   - Keep slide frontmatter minimal
   - Use consistent layout names

2. **Content Organization**
   - One main idea per slide
   - Use section slides to divide topics
   - Keep code examples concise

3. **Performance**
   - Optimize images (use appropriate sizes)
   - Limit complex animations
   - Use code splitting for large presentations

4. **Accessibility**
   - Add alt text for images
   - Use semantic headings
   - Ensure sufficient contrast

5. **Version Control**
   - Commit slides.md regularly
   - Use meaningful commit messages
   - Keep assets in version control

## File Structure Reference

```
my-presentation/
├── slides.md           # Main presentation file
├── package.json        # Dependencies
├── public/            # Static assets
│   ├── images/
│   └── fonts/
├── components/        # Custom Vue components
├── layouts/           # Custom layouts
├── styles/            # Custom styles
└── slidev.config.ts   # Advanced configuration
```

## Developer Tools & Integrations

**VS Code Extension**
- Install "Slidev" extension for enhanced editing
- Syntax highlighting for slides.md
- Preview integration

**Prettier Plugin**
- Format slides.md with Prettier support
- Consistent code formatting in slides

**Quick Start**
- Use StackBlitz: https://sli.dev/new
- Instant online editing environment

**Technology Stack**
- Vite - Fast build tool
- Vue 3 - Component framework
- UnoCSS - Atomic CSS engine
- MDC Syntax - Simplified component styling

## Troubleshooting

**Slide separator not working:**
- Ensure `---` has blank lines before and after
- Check for extra spaces or tabs

**Frontmatter not parsed:**
- Verify YAML syntax (proper indentation)
- Ensure opening/closing `---` on their own lines

**Code highlighting issues:**
- Check language identifier is valid
- Ensure backticks are properly formatted
- Verify Shiki supports the language

**Layout not found:**
- Check theme documentation for available layouts
- Verify spelling matches exactly
- Use `default` as fallback

**Theme not auto-installing:**
- Ensure internet connection
- Manually install: `npm install @slidev/theme-[name]`
- Check theme name spelling in frontmatter

**Interactive features not working in exports:**
- Export formats (PDF, PPTX, PNG) are static
- Use SPA build (`npm run build`) for interactivity
- Host as web app for full feature support

## Useful Commands

```bash
# Start dev server
npm run dev

# Build for production (SPA)
npm run build

# Export to PDF
npm run export

# Export to PPTX (slides as images + notes)
npm run export --format pptx

# Export to PNG (individual slide images)
npm run export --format png

# Export with click animations
npm run export -- --with-clicks

# Export specific slides
npm run export -- --range 1,6-8,10

# Export with dark theme
npm run export -- --dark

# Format slides.md
npm run format
```

## When to Use This Skill

Use this skill when:
- User mentions "Slidev", "presentation", or "slides"
- Working with `slides.md` files
- Creating technical presentations
- Converting existing content to slides
- Refactoring presentation structure
- Analyzing slide organization
- Adding code examples to presentations
- Setting up new Slidev projects
- Installing or configuring themes
- Adding interactive features (drawing, recording)
- Setting up remote presentations
- Exporting to multiple formats

## References

For detailed documentation and examples, see:
- [REFERENCE.md](REFERENCE.md) - Comprehensive Slidev API reference
- [templates/](templates/) - Example slide templates

---

**Note:** This skill requires Node.js >= 18.0. Install Slidev globally with `npm install -g @slidev/cli` or use project-local installation.
