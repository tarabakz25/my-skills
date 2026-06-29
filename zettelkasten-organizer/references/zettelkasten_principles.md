# Zettelkasten Principles

This document outlines the core principles of the Zettelkasten method and how to apply them when organizing and reviewing notes in Obsidian.

## Core Principles

### 1. Atomicity

**Principle**: Each note should contain exactly ONE idea or concept.

**Why**: Atomic notes are easier to link, reuse, and recombine in different contexts. They form the fundamental building blocks of your knowledge system.

**Guidelines**:
- One note = one idea
- If a note covers multiple distinct concepts, split it into multiple notes
- Notes should be self-contained enough to be understood in isolation
- Aim for 100-300 words for most notes (permanent notes)

**Red Flags**:
- Notes with multiple section headings covering unrelated topics
- Notes that try to be comprehensive reference documents
- Notes that cannot be summarized in a single sentence

**Example**:
```
❌ BAD: "Machine Learning.md" (too broad)
✅ GOOD: "Backpropagation Algorithm.md"
✅ GOOD: "Gradient Descent Optimization.md"
✅ GOOD: "Neural Network Activation Functions.md"
```

### 2. Connectivity

**Principle**: Every note should link to at least 2-3 other notes. The value of a note increases with its connections.

**Why**: Isolated notes are lost notes. Connections create context, enable serendipitous discovery, and mirror how memory works.

**Guidelines**:
- Minimum 2-3 links per note (both outgoing and incoming)
- Hub notes (index/MOC notes) should have 10+ connections
- Bidirectional links strengthen the knowledge graph
- Link to notes that provide context, examples, or contrasting ideas

**Types of Links**:
1. **Sequential links**: Connect notes in a logical sequence
   - "This concept builds on [[prerequisite-concept]]"
   - "The next step is [[next-concept]]"

2. **Related concept links**: Connect similar or complementary ideas
   - "See also [[related-concept]]"
   - "This relates to [[parallel-concept]]"

3. **Source links**: Reference where ideas came from
   - "Source: [[book-notes-atomic-habits]]"

4. **Index links**: Connect to hub/MOC notes
   - "Part of [[machine-learning-index]]"

**Red Flags**:
- Notes with 0 links (orphaned notes)
- Notes with only 1 link (weak connections)
- Links without context (why are they linked?)

### 3. Progressive Elaboration

**Principle**: Notes evolve over time. Start small, elaborate as understanding deepens.

**Why**: You don't need to know everything before creating a note. Ideas develop through revisitation and connection.

**Note Types**:

1. **Fleeting Notes** (Temporary)
   - Quick captures of ideas
   - Inbox items to process later
   - Usually deleted or converted after processing
   - Location: `/fleeting/` or `/inbox/`

2. **Literature Notes** (Source-specific)
   - Notes from reading/learning
   - Summarize source material in your own words
   - Include source reference
   - Location: `/sources/` or `/literature/`

3. **Permanent Notes** (Evergreen)
   - Fully developed ideas in your own words
   - Connected to multiple other notes
   - Atomic and self-contained
   - Location: main vault or `/permanent/`

4. **Hub Notes / MOCs** (Maps of Content)
   - Index notes that organize related permanent notes
   - Provide overview and navigation
   - Created when you have 10+ related notes on a topic
   - Location: `/hubs/` or `/MOCs/`

**Workflow**:
```
Fleeting Note → Literature Note → Permanent Note → Hub Note
  (minutes)       (hours/days)      (days/weeks)     (months)
```

### 4. Unique Identifiers

**Principle**: Each note must have a unique, stable, immutable identifier.

**Why**: Allows notes to be renamed without breaking links. Ensures notes can always be referenced.

**Common ID Schemes**:

1. **Timestamp-based** (Luhmann-style)
   - Format: `YYYYMMDDHHMMSS.md` or `YYYYMMDDHHmm.md`
   - Example: `202401061445.md`
   - Pros: Naturally unique, chronological
   - Cons: Not human-readable

2. **UID + Title**
   - Format: `YYYYMMDD-descriptive-title.md`
   - Example: `20240106-backpropagation-algorithm.md`
   - Pros: Unique and readable
   - Cons: Longer filenames

3. **Simple counter**
   - Format: `001-title.md`, `002-title.md`
   - Pros: Short, simple
   - Cons: Requires tracking counter

**Best Practices**:
- Choose one scheme and stick to it consistently
- Never change a note's ID after creation
- Use note titles for human readability (can be changed freely)
- Include ID in YAML frontmatter if using title-based filenames

### 5. Own Your Words

**Principle**: Write notes in your own words, not direct quotes or copy-paste.

**Why**: The act of reformulating strengthens understanding. Your notes should reflect your thinking, not just source material.

**Guidelines**:
- Paraphrase concepts in your own words
- Add your interpretation and context
- Use quotes sparingly and only when the original wording matters
- Always attribute sources but don't just copy them

**Template**:
```markdown
# Concept in My Words

[Explanation in your own words]

## My Understanding
[Your interpretation, examples, questions]

## Connections
- Links to related notes
- How this connects to what you already know

## Source
[[source-note]] - Chapter 3, p. 45
```

### 6. Bi-Directional Linking

**Principle**: When you link from Note A to Note B, consider adding a backlink from B to A.

**Why**: Creates a stronger network and makes relationships explicit in both directions.

**Obsidian Advantage**:
- Obsidian automatically shows backlinks
- But explicit links in content provide context

**Best Practice**:
```markdown
# Note A: Neural Networks
Neural networks use [[backpropagation]] to learn.

# Note B: Backpropagation
Backpropagation is used to train [[neural-networks]].
```

## Quality Criteria Checklist

Use this checklist when reviewing notes:

### Structure Quality
- [ ] Note has a unique, stable identifier
- [ ] Note covers exactly one concept (atomic)
- [ ] Note is self-contained and understandable
- [ ] Note has descriptive title
- [ ] Note has proper YAML frontmatter

### Content Quality
- [ ] Content is in your own words (not copy-paste)
- [ ] Content is clear and concise (100-300 words ideal)
- [ ] Content includes your interpretation/understanding
- [ ] Content includes examples or applications (if relevant)
- [ ] Sources are properly attributed

### Connectivity Quality
- [ ] Note has at least 2-3 outgoing links
- [ ] Note has at least 1-2 incoming links (backlinks)
- [ ] Links are contextual (explain why they're related)
- [ ] Note connects to relevant hub/MOC notes
- [ ] Bidirectional relationships are established

### Metadata Quality
- [ ] Has creation date
- [ ] Has relevant tags (2-5 tags ideal)
- [ ] Has note type (fleeting/literature/permanent)
- [ ] Has status (if using staged workflow)

## Common Anti-Patterns to Avoid

### 1. Collector's Fallacy
**Problem**: Saving/clipping without processing
**Solution**: Always create a literature note with YOUR interpretation

### 2. Orphan Notes
**Problem**: Creating notes without linking them
**Solution**: Link new notes to at least 2 existing notes immediately

### 3. Premature Optimization
**Problem**: Spending too much time on perfect organization
**Solution**: Focus on connections, not folder structure

### 4. Direct Quotes Library
**Problem**: Notes are just collections of quotes
**Solution**: Write in your own words; use quotes sparingly

### 5. Broad Topic Notes
**Problem**: Creating "Machine Learning.md" instead of atomic notes
**Solution**: Split into atomic concepts

### 6. No Hub Notes
**Problem**: Having 50 notes on a topic without an index
**Solution**: Create MOC/hub notes when you have 10+ related notes

### 7. Link Hoarding
**Problem**: Adding links without context
**Solution**: Explain WHY notes are connected

## Recommended Frontmatter Structure

```yaml
---
id: 202401061445                    # Unique identifier
title: "Backpropagation Algorithm"  # Human-readable title
created: 2024-01-06                 # Creation date
modified: 2024-01-06                # Last modification
tags:                               # 2-5 relevant tags
  - machine-learning
  - neural-networks
  - algorithms
type: permanent                     # fleeting/literature/permanent/hub
status: developing                  # seedling/developing/evergreen
source: "[[deep-learning-book]]"    # Optional: source reference
---
```

## Progressive Development Stages

### Seedling
- Just created
- Basic idea captured
- 1-2 connections
- <100 words

### Developing
- Being actively worked on
- Core idea elaborated
- 3-5 connections
- 100-200 words
- Own interpretation added

### Evergreen
- Mature note
- Well-connected (5+ connections)
- Clear and comprehensive
- 200-300 words
- Multiple revisions
- Referenced by other notes

## Review Process

### Daily Review (5-10 minutes)
- Process fleeting notes → literature notes
- Link new notes to existing notes
- Identify orphans and connect them

### Weekly Review (20-30 minutes)
- Convert literature notes → permanent notes
- Identify clusters that need hub notes
- Check for broken links
- Review underdeveloped notes

### Monthly Review (1-2 hours)
- Comprehensive quality assessment
- Create/update hub notes
- Identify knowledge gaps
- Refactor and consolidate if needed

## Tools and Commands

### Finding Issues
```bash
# Find orphaned notes (no links)
rg --files-without-match '\[\[.*\]\]' *.md

# Find notes without tags
rg --files-without-match '^tags:' *.md

# Find very short notes
find . -name "*.md" -type f -exec wc -w {} \; | awk '$1 < 20'

# Count outgoing links per note
rg -c '\[\[.*\]\]' *.md
```

### Graph Analysis (using our scripts)
```bash
# Basic analysis
python3 ~/.claude/skills/zettelkasten-organizer/scripts/analyze_vault.py

# Comprehensive review
python3 ~/.claude/skills/zettelkasten-organizer/scripts/review_zettelkasten.py

# Find orphans only
python3 ~/.claude/skills/zettelkasten-organizer/scripts/analyze_vault.py --orphans-only
```

## Further Reading

- Ahrens, S. (2017). *How to Take Smart Notes*
- Luhmann's original Zettelkasten system
- Obsidian documentation: https://help.obsidian.md/
- Andy Matuschak's notes on evergreen notes: https://notes.andymatuschak.org/

## Summary

A healthy Zettelkasten is characterized by:
- **Atomic notes**: One idea per note
- **Rich connections**: Every note links to multiple others
- **Progressive development**: Notes evolve from fleeting to evergreen
- **Consistent structure**: Uniform IDs, metadata, and formatting
- **Original thinking**: Notes in your own words
- **Regular maintenance**: Daily processing, weekly review

The goal is not perfection but a living, breathing knowledge system that grows with you.
