# Feature Spec Template

```markdown
---
title: {Feature Name}
type: feature
status: draft
author: {author}
created: {YYYY-MM-DD}
related: []
---

# {Feature Name}

## 1. Overview

### 1.1 Purpose / Background
{Why this feature is needed. The problem it solves and business value, in 1-3 paragraphs}

### 1.2 Target Users
- {Persona 1: role, usage scenario}
- {Persona 2: role, usage scenario}

### 1.3 Scope
**In scope:**
- {Included features / scope}

**Out of scope:**
- {Explicitly excluded items / future considerations}

### 1.4 Glossary
| Term | Definition |
|------|-----------|
| {term} | {definition} |

## 2. Functional Requirements

### 2.1 User Stories
- US-001: As a {role}, I want to {goal}, so that {value}
- US-002: ...

### 2.2 Main Flow
{Screen transition diagram or numbered steps}

1. User performs {action on screen}
2. System executes {process}
3. System displays {result}

### 2.3 Screens / UI
| Screen ID | Screen Name | Main Inputs | Main Outputs | Next Screen |
|-----------|------------|------------|-------------|-------------|
| SC-001 | {screen name} | {input fields} | {display content} | {next screen} |

### 2.4 State Transitions
{For features with state, document states and transition conditions}

```
[Initial] --(condition1)--> [In Progress] --(condition2)--> [Completed]
                                |
                           (Cancel)
                                v
                           [Cancelled]
```

## 3. Non-Functional Requirements

### 3.1 Performance
- Screen load: p95 under {N}ms
- Concurrent users: {N}
- Data throughput: {N items/sec}

### 3.2 Security
- Authentication: {method}
- Authorization: {policy}
- Input validation: {validation rules}
- Sensitive data: {handling policy}

### 3.3 Availability
- SLA: {uptime}
- Failure behavior: {fallback / error display}
- Data consistency: {transaction boundaries}

### 3.4 Monitoring / Logging
- Logged events: {what to record}
- Alert conditions: {what triggers notification}

### 3.5 Scalability
- Projected growth: {Nx over N years}
- Scaling strategy: {horizontal / vertical approach}

## 4. Edge Cases / Error States

### 4.1 Boundary Values
- {Behavior for: 0 items / max items / empty string / max length}

### 4.2 Concurrency / Race Conditions
- {Behavior when multiple users operate on the same resource}

### 4.3 Network / Timeout
- {Retry logic and timeout settings on communication failure}

### 4.4 Invalid Input
- {Handling of: wrong type / null / undefined / unexpected values}

### 4.5 Permission / Auth Errors
- {Behavior for: unauthenticated / insufficient permissions / session expiry}

## 5. Acceptance Criteria

### AC-001: Happy Path
- **Given** {preconditions}
- **When** {action}
- **Then** {expected result}

### AC-002: Error Path
- **Given** {preconditions}
- **When** {invalid action}
- **Then** {error message / recovery path}

## 6. Dependencies / Assumptions
- Existing features: {dependent features}
- External systems: {integrated APIs / services}
- Prerequisites: {what must be in place before implementation}

## 7. Risks / Open Questions
- Risk: {implementation risk / mitigation}
- Open: {undecided items / decision maker / deadline}

## 8. Change History
| Date | Change | Author |
|------|--------|--------|
| {YYYY-MM-DD} | Initial draft | {author} |
```