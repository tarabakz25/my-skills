---
name: zettelkasten-organizer
description: Organize and review Obsidian vault notes following Zettelkasten framework. Use when working with Obsidian vaults, reviewing note structure, checking links, or when the user mentions Zettelkasten, note organization, or vault cleanup.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Zettelkasten Organizer

A skill for organizing and reviewing Obsidian vault notes according to Zettelkasten principles.

## Overview

This skill helps maintain a well-structured Zettelkasten system in your Obsidian vault by:
- Analyzing vault structure and note organization
- Validating naming conventions and metadata
- Checking link integrity and relationships
- Identifying orphaned or weakly connected notes
- Suggesting improvements and connections
- Ensuring compliance with vault-specific rules

## Instructions

### Step 1: Understand the Vault Rules

Before performing any analysis:
1. Look for rule documentation in the vault (common locations: `README.md`, `Rules.md`, `Zettelkasten.md`, `.obsidian/` folder)
2. Read and understand:
   - Note naming conventions (timestamp format, ID scheme, etc.)
   - Required YAML frontmatter fields
   - Link structure requirements
   - Tag taxonomy
   - Folder organization
3. If rules are unclear, ask the user for clarification

### Step 2: Run Initial Analysis

Execute the vault analysis script to gather baseline metrics:

```bash
python3 ~/.claude/skills/zettelkasten-organizer/scripts/analyze_vault.py
```

This will provide:
- Total note count and distribution
- Link statistics (incoming/outgoing)
- Orphaned notes
- Broken links
- YAML frontmatter compliance
- Naming convention violations

### Step 3: Review and Categorize Issues

Based on the analysis output, categorize issues by severity:

**Critical Issues** (fix immediately):
- Broken links (references to non-existent notes)
- Missing required frontmatter fields
- Naming convention violations

**Important Issues** (should fix):
- Orphaned notes (no incoming or outgoing links)
- Weakly connected notes (<2 connections)
- Inconsistent tag usage
- Missing or incomplete metadata

**Optimization Opportunities**:
- Potential connections between related notes
- Tag consolidation
- Structure improvements

### Step 4: Execute Zettelkasten Review

Run the comprehensive review script:

```bash
python3 ~/.claude/skills/zettelkasten-organizer/scripts/review_zettelkasten.py
```

This script performs:
- Link graph analysis
- Content quality assessment
- Connection strength evaluation
- Cluster identification
- Recommendation generation

### Step 5: Present Findings and Recommendations

Organize your findings in a clear, actionable format:

1. **Executive Summary**: High-level overview of vault health
2. **Critical Issues**: List with specific file paths and line numbers
3. **Recommendations**: Prioritized list of improvements
4. **Potential Connections**: Suggested links between related notes

For each issue, provide:
- File path with line number reference (e.g., `notes/202401011200.md:5`)
- Description of the problem
- Suggested fix with example code/text
- Rationale based on Zettelkasten principles

### Step 6: Assist with Implementation

Offer to help implement fixes:
- Create missing backlinks
- Fix broken links
- Update frontmatter
- Reorganize tags
- Create index notes for clusters

Always ask for confirmation before modifying files.

## Key Zettelkasten Principles to Check

Reference `references/zettelkasten_principles.md` for detailed guidelines.

### Atomicity
- Each note should contain ONE idea
- Notes should be self-contained
- Check for notes that try to cover multiple topics

### Connectivity
- Every note should link to at least 2-3 other notes
- Bidirectional links strengthen the network
- Hub notes should exist for major topics

### Progressive Elaboration
- Notes should reference sources
- Ideas should be developed across multiple linked notes
- Check for notes that are too brief or underdeveloped

### Unique Identifiers
- Consistent ID scheme (timestamp, UID, etc.)
- No duplicate IDs
- IDs should be immutable

## Examples

### Example 1: Basic Vault Review

**User**: "Review my Zettelkasten vault"

**Actions**:
1. Check for `README.md` or rules document
2. Run `analyze_vault.py`
3. Run `review_zettelkasten.py`
4. Present findings:
   ```
   Vault Health Report
   ==================

   Total Notes: 347
   Orphaned Notes: 12
   Broken Links: 5
   Average Connections: 4.2

   Critical Issues:
   - notes/202401051430.md:1 - Broken link to [[non-existent-note]]
   - notes/fleeting/20240106.md - Missing required 'tags' frontmatter

   Recommendations:
   1. Fix broken links (see list above)
   2. Connect orphaned notes to the network
   3. Create hub note for "machine learning" cluster (23 related notes)
   ```

### Example 2: Link Structure Analysis

**User**: "Find orphaned notes in my vault"

**Actions**:
1. Run `analyze_vault.py --orphans-only`
2. Present orphaned notes with connection suggestions:
   ```
   Orphaned Notes (no links):
   ==========================

   1. notes/202312151200.md - "Neural Network Basics"
      Suggested connections:
      - [[202312201130]] Deep Learning Introduction
      - [[202401021045]] Backpropagation Explained

   2. notes/202401031615.md - "Reading Notes: Clean Code"
      Suggested connections:
      - [[202312281400]] Software Engineering Principles
      - Create new hub note: "Programming Best Practices"
   ```

### Example 3: Metadata Validation

**User**: "Check if all my notes have proper frontmatter"

**Actions**:
1. Read vault rules for required frontmatter fields
2. Run validation check
3. Report violations:
   ```
   Frontmatter Validation Report
   =============================

   Required fields: tags, created, type

   Missing fields:
   - notes/202401041200.md - Missing 'type' field
   - notes/202401051500.md - Missing 'tags' and 'created'

   Invalid values:
   - notes/202401021100.md:3 - 'created: "yesterday"' (expected YYYY-MM-DD format)
   ```

   Offer to fix automatically with user confirmation.

## Error Handling

- If Python scripts are not executable, suggest running: `chmod +x ~/.claude/skills/zettelkasten-organizer/scripts/*.py`
- If dependencies are missing, provide installation instructions
- If vault path is ambiguous, confirm with user
- Always validate before making bulk changes

## Tips for Best Results

1. **Start with rules**: Always read vault-specific rules first
2. **Incremental fixes**: Fix critical issues before optimization
3. **Preserve content**: Never delete notes without explicit permission
4. **Explain rationale**: Connect recommendations to Zettelkasten principles
5. **Show examples**: Provide concrete examples of fixes
6. **Respect workflow**: Don't enforce rigid structure if user has working system

## Limitations

- This skill analyzes structure, not content quality (use AI to review content)
- Cannot automatically determine semantic relationships (can suggest based on keywords/tags)
- Graph visualization requires external tools (can generate stats/data)
- Large vaults (>1000 notes) may require performance optimization
