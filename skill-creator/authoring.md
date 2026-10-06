# Skill authoring reference

Detailed guidance for `make-skill`. Read when writing descriptions, choosing patterns, or needing a full example.

## Description examples

```yaml
# PDF Processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Excel Analysis
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git Commit Helper
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.

# Code Review
description: Review code for quality, security, and best practices following team standards. Use when reviewing pull requests, code changes, or when the user asks for a code review.
```

## Concise vs verbose

**Good (concise):**
```markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Bad (verbose):** lecturing what a PDF is, listing every library, then maybe getting to the point.

Challenge each piece: Does the agent need this? Can we assume it? Does the paragraph earn its tokens?

## Degrees of freedom

| Freedom | When | Example |
|---------|------|---------|
| **High** (text) | Multiple valid approaches | Code review guidelines |
| **Medium** (templates) | Preferred pattern, some variation | Report generation |
| **Low** (scripts) | Fragile / must be consistent | Migrations, validators |

## Common patterns

### Template

```markdown
## Report structure

Use this template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with supporting data

## Recommendations
1. Specific actionable recommendation
```
```

### Examples (when quality depends on seeing format)

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```
```

### Workflow checklist

```markdown
## Form filling workflow

```
Task Progress:
- [ ] Step 1: Analyze the form
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill the form
- [ ] Step 5: Verify output
```

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`
```

### Conditional workflow

```markdown
1. **Creating new content?** → Creation workflow
2. **Editing existing content?** → Editing workflow
```

### Feedback loop

```markdown
1. Make edits
2. Validate: `python scripts/validate.py output/`
3. On failure: fix → re-validate
4. Proceed only when validation passes
```

## Utility scripts

Prefer bundled scripts when consistency matters:

- More reliable than generated code
- Save tokens and time
- Same behavior across uses

Document whether the agent should **execute** (usual) or **read** as reference.

```markdown
**validate.py**: Check for errors
```bash
python scripts/validate.py fields.json
# Returns: "OK" or lists conflicts
```
```

## Anti-patterns

1. **Windows-style paths** — use `scripts/helper.py`, not `scripts\helper.py`
2. **Too many options** — one default + escape hatch
3. **Time-sensitive “before DATE”** — use current / old-patterns sections instead
4. **Inconsistent terms** — pick one word per concept and stick to it
5. **Vague names** — `processing-pdfs` ✅; `helper` / `utils` ❌

## Complete example

**Directory:**
```
code-review/
├── SKILL.md
├── STANDARDS.md
└── examples.md
```

**SKILL.md:**
```markdown
---
name: code-review
description: Review code for quality, security, and maintainability following team standards. Use when reviewing pull requests, examining code changes, or when the user asks for a code review.
---

# Code Review

## Quick Start

1. Check for correctness and potential bugs
2. Verify security best practices
3. Assess readability and maintainability
4. Ensure tests are adequate

## Review Checklist

- [ ] Logic is correct and handles edge cases
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)
- [ ] Code follows project style conventions
- [ ] Functions are appropriately sized and focused
- [ ] Error handling is comprehensive
- [ ] Tests cover the changes

## Providing Feedback

- 🔴 **Critical**: Must fix before merge
- 🟡 **Suggestion**: Consider improving
- 🟢 **Nice to have**: Optional enhancement

## Additional Resources

- [STANDARDS.md](STANDARDS.md)
- [examples.md](examples.md)
```
