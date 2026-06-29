# Slidev Skill for Claude Code

A comprehensive skill for working with Slidev presentations.

## Overview

This skill enables Claude Code to help you create, edit, analyze, and refactor Slidev presentations. Slidev is a web-based presentation tool for developers that uses Markdown and Vue.js.

## Features

### 1. Slide Creation & Editing
- Initialize new Slidev projects
- Add new slides to existing presentations
- Edit slide content and frontmatter
- Configure themes, layouts, and styling

### 2. Structure Analysis
- Parse and analyze slides.md files
- Display slide organization and hierarchy
- List all slides with their layouts
- Identify themes, transitions, and configurations

### 3. Refactoring Support
- Reorder slides
- Standardize frontmatter across slides
- Optimize layouts for better presentation
- Consolidate duplicate configurations

## Usage

The skill activates automatically when you:
- Mention "Slidev", "presentation", or "slides"
- Work with `slides.md` files
- Request presentation-related tasks

### Example Commands

```
Create a new Slidev presentation about TypeScript
```

```
Analyze the structure of my slides.md file
```

```
Add a new slide with code examples
```

```
Refactor my presentation to use consistent layouts
```

## Templates

This skill includes three ready-to-use templates:

### 1. Basic Template (`templates/basic.md`)
A general-purpose presentation template with:
- Cover slide
- Table of contents
- Section dividers
- Two-column layouts
- Quote slides
- Fact/statistic slides

### 2. Tech Talk Template (`templates/tech-talk.md`)
For technical presentations with:
- Code examples with syntax highlighting
- Diagrams (Mermaid)
- Mathematical formulas (LaTeX)
- Architecture diagrams
- Performance benchmarks
- API documentation examples
- Live code editor (Monaco)

### 3. Minimal Template (`templates/minimal.md`)
A bare-bones template for quick starts:
- Simple cover slide
- Basic content slides
- No complex configurations

## Reference Documentation

See [REFERENCE.md](REFERENCE.md) for:
- Complete frontmatter options
- All built-in layouts
- Code block features
- Animation and transition syntax
- Theme configuration
- Advanced features

## Getting Started

### Prerequisites

- Node.js >= 18.0
- npm, pnpm, or yarn

### Initialize a New Project

```bash
npm init slidev@latest
cd my-presentation
npm install
npm run dev
```

### Use a Template

Copy one of the templates to your project:

```bash
cp ~/.claude/skills/slidev/templates/tech-talk.md ./slides.md
```

## File Structure

```
~/.claude/skills/slidev/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── REFERENCE.md          # Comprehensive API reference
├── templates/
│   ├── basic.md          # Basic presentation template
│   ├── tech-talk.md      # Technical presentation template
│   └── minimal.md        # Minimal template
└── examples/
    └── (future examples)
```

## Common Tasks

### Create a New Presentation

Ask Claude Code:
```
Create a new Slidev presentation about [topic]
```

### Analyze Existing Slides

Ask Claude Code:
```
Analyze my slides.md and show me the structure
```

### Add Slides

Ask Claude Code:
```
Add a new slide about [topic] with [layout]
```

### Refactor

Ask Claude Code:
```
Refactor my presentation to use consistent frontmatter
```

## Best Practices

1. **One idea per slide** - Keep slides focused
2. **Use semantic layouts** - Choose appropriate layouts for content
3. **Consistent styling** - Use frontmatter consistently
4. **Version control** - Commit slides.md to git
5. **Optimize images** - Use appropriate image sizes
6. **Test responsiveness** - Check on different screen sizes

## Slidev Resources

- Official Website: https://sli.dev
- Documentation: https://sli.dev/guide/
- GitHub: https://github.com/slidevjs/slidev
- Theme Gallery: https://sli.dev/themes/gallery
- Discord Community: https://chat.sli.dev

## Keyboard Shortcuts

During presentation mode:

- `Space` / `→` - Next slide
- `←` - Previous slide
- `f` - Fullscreen
- `o` - Overview mode
- `d` - Dark mode toggle
- `g` - Go to slide (enter number)
- `c` - Camera/recording
- `Esc` - Exit modes

## Export Options

### PDF Export
```bash
npm run export
npm run export -- --output my-slides.pdf
```

### SPA Build
```bash
npm run build
# Output in dist/
```

## Troubleshooting

**Slides not separated correctly:**
- Ensure `---` has blank lines before and after

**Frontmatter not working:**
- Check YAML syntax and indentation
- Verify opening/closing `---` on separate lines

**Layout not found:**
- Verify layout name matches theme documentation
- Check theme is installed correctly

**Code highlighting issues:**
- Ensure language identifier is supported
- Check backtick formatting

## License

This skill follows the same license as Claude Code.

## Contributing

This skill is part of your personal Claude Code configuration. Feel free to modify and enhance it for your needs.

---

For questions or issues, refer to the [Claude Code documentation](https://code.claude.com/docs).
