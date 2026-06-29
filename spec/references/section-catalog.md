# Spec Section Catalog

Use this catalog during `/spec create` Phase 1.5 (Sizing) to decide which sections to include. **Do not copy the full template every time.**

## Complexity Tiers

| Tier | When to use | Target length |
|------|-------------|---------------|
| `minimal` | Single behavior change, config toggle, small UI tweak, one endpoint, ≤3 SPEC items | ~50–120 lines |
| `standard` | Multi-step flow, several endpoints, moderate domain logic, 4–15 SPEC items | ~120–250 lines |
| `full` | Cross-cutting system, new subsystem, compliance/security-critical, 15+ SPEC items | 250+ lines |

Infer tier from scope; confirm with user only when ambiguous (e.g., "small change" but touches auth + billing).

## Universal Sections (all types)

| Section | minimal | standard | full | Include when |
|---------|---------|----------|------|--------------|
| Overview (purpose, scope) | ✅ | ✅ | ✅ | Always |
| Glossary | ⬜ | ⚠️ | ✅ | 3+ domain terms OR cross-team doc |
| Functional requirements | ✅ | ✅ | ✅ | Always |
| Acceptance criteria (GWT) | ✅ | ✅ | ✅ | Always |
| Spec Items table | ✅ | ✅ | ✅ | Always |
| Dependencies / assumptions | ⚠️ | ✅ | ✅ | External systems, libs, or prior specs involved |
| Risks / open questions | ⚠️ | ✅ | ✅ | Any unresolved item after feasibility gate |
| Change history | ⬜ | ⚠️ | ✅ | `full` or long-lived spec expected to revise |

Legend: ✅ include · ⚠️ include if relevant · ⬜ omit (note reason in `## Excluded Sections`)

## Feature-type Sections

| Section | minimal | standard | full | Include when |
|---------|---------|----------|------|--------------|
| Target users / personas | ⬜ | ✅ | ✅ | Multiple roles or permission differences |
| User stories (US-NNN) | ⬜ | ✅ | ✅ | 2+ distinct user goals |
| Main flow | ✅ | ✅ | ✅ | Always (1–5 steps OK for minimal) |
| Screens / UI table | ⬜ | ⚠️ | ✅ | UI changes; skip for backend-only |
| State transitions | ⬜ | ⚠️ | ✅ | Stateful entity (order, job, session, etc.) |
| NFR: Performance | ⬜ | ⚠️ | ✅ | Latency/throughput matters or user stated SLA |
| NFR: Security | ⬜ | ⚠️ | ✅ | Auth, PII, payments, or admin actions |
| NFR: Availability | ⬜ | ⬜ | ⚠️ | Production-critical or SLA stated |
| NFR: Monitoring | ⬜ | ⬜ | ⚠️ | Ops/alerting requirements or `full` tier |
| NFR: Scalability | ⬜ | ⬜ | ✅ | Expected load growth or multi-tenant |
| Edge cases (full §4) | ⚠️ | ✅ | ✅ | Minimal: only edges that change behavior |
| Concurrency / race | ⬜ | ⚠️ | ✅ | Shared mutable resource |
| Network / timeout | ⬜ | ⚠️ | ✅ | External API or async jobs |

## API-type Sections

| Section | minimal | standard | full | Include when |
|---------|---------|----------|------|--------------|
| Endpoint list table | ✅ | ✅ | ✅ | Always |
| Per-endpoint detail blocks | ⚠️ | ✅ | ✅ | Minimal: detail only changed endpoints |
| Common spec (base URL, auth) | ⚠️ | ✅ | ✅ | New API surface; else reference existing spec |
| Error response matrix | ⚠️ | ✅ | ✅ | Minimal: errors for changed endpoints only |
| NFR: Performance | ⬜ | ⚠️ | ✅ | Public or high-traffic API |
| NFR: Rate limiting | ⬜ | ⚠️ | ✅ | External consumers or abuse risk |
| NFR: Versioning | ⬜ | ⚠️ | ✅ | Breaking change or v2 |
| Idempotency / concurrency | ⬜ | ⚠️ | ✅ | POST/PUT with side effects |

## System-type Sections

| Section | minimal | standard | full | Include when |
|---------|---------|----------|------|--------------|
| Architecture diagram | ⬜ | ✅ | ✅ | 2+ components or new integration |
| Component list | ⬜ | ✅ | ✅ | Same as above |
| Data flow / sequence | ⬜ | ⚠️ | ✅ | Async, events, or multi-hop requests |
| Deployment / infra | ⬜ | ⬜ | ✅ | New runtime, region, or env |
| ADR / trade-offs | ⬜ | ⚠️ | ✅ | Non-obvious technology choice |

## Data-type Sections

| Section | minimal | standard | full | Include when |
|---------|---------|----------|------|--------------|
| ER diagram | ⬜ | ⚠️ | ✅ | 2+ entities or new relationships |
| Entity column tables | ✅ | ✅ | ✅ | Always for changed entities |
| Indexes | ⚠️ | ✅ | ✅ | Query patterns or scale stated |
| Migration / rollout | ⚠️ | ✅ | ✅ | Schema change in production |
| Data retention / privacy | ⬜ | ⚠️ | ✅ | PII, GDPR, or audit requirements |

## Excluded Sections Block

When omitting a template section, append to the spec (after Overview):

```markdown
## Excluded Sections

| Section | Reason |
|---------|--------|
| NFR: Scalability | Single-user admin tool; no growth requirement stated |
| Screens / UI | Backend-only API change |
```

Do **not** fill omitted sections with "N/A" placeholders — exclusion table is enough for `minimal`/`standard`.
