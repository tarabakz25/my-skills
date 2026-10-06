---
name: make-skill
description: >-
  Create or update Agent Skills (SKILL.md structure, descriptions, workflows,
  progressive disclosure, audit checklist). Use when authoring a new skill,
  improving/refactoring an existing skill, auditing skill-builder compliance,
  or when the user says /make-skill, /skill-builder, /skill-updater,
  /create-skill, or 「スキル更新」.
disable-model-invocation: true
---

# Make Skill

Create **or** update Agent Skills. One entry point for both flows.

| Mode | When | Default flow |
|------|------|----------------|
| **Create** | New skill from scratch | Discovery → Design → Implement → Verify |
| **Update** | Existing skill | Audit → Approve → Apply → Re-audit |

For patterns, anti-patterns, and a full example, see [authoring.md](authoring.md).

## When to use

- User names this skill (`/make-skill`, `/skill-builder`, `/skill-updater`, `/create-skill`, 「スキル更新」)
- Authoring a new skill or asking about `SKILL.md` structure
- Improving, refactoring, or auditing an existing skill

## Mode select

1. **Creating new content?** → [Create](#create)
2. **Editing an existing skill?** → [Update](#update)
3. Unclear → ask once: create vs update (and target path/name if update)

Never write into `~/.cursor/skills-cursor/` (Cursor built-ins).

### Verbatim text

If the user includes exact wording, use it **verbatim** in `SKILL.md` (same words, same order). Do not paraphrase, soften, or expand their copy.

### Inferring from context

If conversation already defined the workflow, infer the skill from that context instead of re-asking everything.

---

## Shared: locations & structure

```
skill-name/
├── SKILL.md              # Required
├── reference.md          # Optional
├── examples.md           # Optional
└── scripts/              # Optional
```

| Type | Path |
|------|------|
| Personal | `~/.skills/skill-name/` |
| Project | `.cursor/skills/skill-name/` or `.skills/skill-name/` |

### SKILL.md frontmatter

```markdown
---
name: your-skill-name
description: Brief description of what this skill does and when to use it
disable-model-invocation: true
---
```

| Field | Requirements |
|-------|--------------|
| `name` | ≤64 chars, lowercase letters/numbers/hyphens only |
| `description` | ≤1024 chars, non-empty, third person, **WHAT + WHEN**, trigger terms |

Default `disable-model-invocation: true` (explicit load only). Omit only when auto-invoke is intentional.

### Description rules (critical)

- Third person: ✅ "Processes Excel files…" ❌ "I can…" / "You can use…"
- Specific + triggers: include domain keywords the agent will match
- Both WHAT (capabilities) and WHEN (scenarios)

### Authoring principles (short)

1. **Concise** — agent is already smart; only add what it wouldn't know
2. **SKILL.md under ~500 lines** — move detail to sibling files
3. **Progressive disclosure** — essentials in `SKILL.md`; links **one level deep**
4. **Degrees of freedom** — high (guidelines) / medium (templates) / low (scripts) by fragility
5. **One default + escape hatch** — avoid listing many equivalent options
6. **No fragile "before DATE"** — use "current / old patterns" instead

---

## Create

### Inputs to gather

If missing:

1. Purpose and scope
2. Target location (personal vs project)
3. Trigger scenarios
4. Key domain knowledge the agent wouldn't already know
5. Output format / templates
6. Existing patterns to follow

Use AskQuestion when available; otherwise ask briefly.

### Workflow

```
Progress:
- [ ] 1. Discovery
- [ ] 2. Design (name, description, sections, supporting files?)
- [ ] 3. Implement (directory + SKILL.md + siblings)
- [ ] 4. Verify (checklist below)
```

**Design:** lowercase hyphenated name ≤64 chars; third-person description with triggers; outline sections; decide scripts vs prose.

**Implement:** create dir under the chosen location; write frontmatter + body; add references/scripts only when needed.

**Prefer extending** an existing skill over duplicating (~80% overlap rule).

---

## Update

### Inputs to gather

If missing:

1. **Target skill** — path or name (resolve personal under `~/.skills/<name>/`)
2. **Intent** — audit only, apply specific changes, or both (default: both)
3. **Change brief** — what to add/change/remove (optional if audit-only)
4. **Verbatim text** — if provided, use verbatim

### Workflow

```
Progress:
- [ ] 1. Locate (SKILL.md + siblings)
- [ ] 2. Audit against checklist
- [ ] 3. Present findings + proposed plan
- [ ] 4. Get approval (unless user already said apply)
- [ ] 5. Apply edits
- [ ] 6. Re-audit and report
```

### Propose format

```markdown
## Audit: <skill-name>

### Findings
- 🔴 Blocker: ...
- 🟡 Should-fix: ...
- 🟢 Nice-to-have: ...

### Proposed changes
1. ...

### Out of scope / unchanged
- ...
```

| Level | Meaning |
|-------|---------|
| **Blocker** | Breaks discovery, metadata, or core usability — fix before done |
| **Should-fix** | Clear authoring violation — fix unless user opts out |
| **Nice-to-have** | Optional polish |

Do not apply until approved, unless the user already requested apply with a clear brief.

### Apply rules

- Preserve intent and working workflows
- Prefer editing existing files over adding new ones
- Split out of `SKILL.md` when over ~500 lines or clearly reference material
- Do not invent domain rules the user did not request
- Do not rename directory/`name` unless asked

### Common update patterns

| Request | Approach |
|---------|----------|
| Better discovery | Rewrite `description` (WHAT + WHEN + triggers) |
| Too long | Split to siblings; keep workflow in `SKILL.md` |
| Unclear steps | Checklist workflow; one default + escape hatch |
| New capability | Add only the requested section; update description triggers |
| Compliance pass | Fix blockers/should-fixes; list nice-to-haves |

---

## Audit / verification checklist

Use for Create Phase 4 and Update audit/re-audit.

### Frontmatter
- [ ] `name`: ≤64 chars, lowercase letters/numbers/hyphens only
- [ ] `description`: non-empty, ≤1024 chars, third person, WHAT + WHEN, trigger terms
- [ ] `disable-model-invocation: true` unless auto-invoke is intentional

### Body quality
- [ ] Concise — no lecture the agent already knows
- [ ] `SKILL.md` under ~500 lines
- [ ] Consistent terminology
- [ ] Concrete examples / steps where quality depends on them
- [ ] Clear workflow for multi-step tasks
- [ ] No fragile time-sensitive “before DATE” guidance

### Structure
- [ ] Progressive disclosure; references one level deep
- [ ] Scripts (if any): documented, executable intent clear, Unix paths only

### Description smells (fix if present)
- First/second person; vague with no triggers; missing WHEN

### Scripts (if any)
- [ ] Solve problems rather than punt; packages documented; helpful errors

---

## Done criteria

**Create:** skill discoverable; checklist clean; files in the chosen location.

**Update:** approved changes applied (or audit-only delivered); blockers and agreed should-fixes resolved; brief summary of files touched.

## Additional resources

- Patterns, anti-patterns, description examples, complete sample skill: [authoring.md](authoring.md)
