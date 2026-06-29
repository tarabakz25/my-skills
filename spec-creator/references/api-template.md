# API Spec Template

```markdown
---
title: {API Name}
type: api
status: draft
author: {author}
created: {YYYY-MM-DD}
related: []
---

# {API Name} Specification

## 1. Overview

### 1.1 Purpose / Background
{Problem this API solves}

### 1.2 Consumers
- {Client types: Web app / Mobile / Third-party}

### 1.3 Scope
**In scope / Out of scope**

### 1.4 Glossary
| Term | Definition |
|------|-----------|

## 2. Endpoint Specification

### 2.1 Common Spec
- Base URL: `https://api.example.com/v1`
- Authentication: {Bearer JWT / API Key / OAuth2}
- Content-Type: `application/json`
- Encoding: UTF-8
- DateTime format: ISO 8601 (e.g., `2026-04-27T15:42:00+09:00`)

### 2.2 Endpoint List
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/resources` | List all | Required |
| GET | `/resources/{id}` | Get detail | Required |
| POST | `/resources` | Create | Required |
| PUT | `/resources/{id}` | Update | Required |
| DELETE | `/resources/{id}` | Delete | Required |

### 2.3 Endpoint Details

#### POST /resources

**Description**: {Responsibility of this endpoint}

**Request**
```http
POST /v1/resources HTTP/1.1
Authorization: Bearer ***
Content-Type: application/json

{
  "name": "string",
  "amount": 0
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| name | string | Yes | 1-100 chars | Resource name |
| amount | integer | Yes | >= 0 | Amount |

**Response (Success)**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "uuid",
  "name": "string",
  "amount": 0,
  "createdAt": "2026-04-27T15:42:00+09:00"
}
```

**Response (Error)**
| HTTP Status | code | Trigger |
|-------------|------|---------|
| 400 | `validation_error` | Validation failure |
| 401 | `unauthorized` | Auth error |
| 403 | `forbidden` | Insufficient permissions |
| 409 | `conflict` | Unique constraint violation |
| 429 | `rate_limit_exceeded` | Rate limit exceeded |
| 500 | `internal_error` | Server error |

Common error response format:
```json
{
  "error": {
    "code": "validation_error",
    "message": "name is required",
    "details": []
  }
}
```

## 3. Non-Functional Requirements

### 3.1 Performance
- p50: {N}ms / p95: {N}ms / p99: {N}ms
- Throughput: {N req/sec}

### 3.2 Security
- Authentication: {method}
- Authorization: {RBAC / ABAC scopes}
- Input validation: {validation strategy for all fields}
- Rate limiting: {N req/min per IP or token}
- Transport: TLS 1.2+

### 3.3 Availability
- SLA: {99.9% etc}
- Retry policy: {idempotency key usage}

### 3.4 Monitoring / Logging
- Record: request ID, user ID, response time, status
- Alerts: error rate > N%, p95 > N ms

### 3.5 Versioning
- Strategy: {URL path / header}
- Backward compatibility policy: {deprecation notice period for breaking changes}

## 4. Edge Cases / Error States

### 4.1 Boundary Values
- Behavior for: empty array, max items, empty string, max-length string

### 4.2 Concurrency / Idempotency
- Handling duplicate requests with the same Idempotency-Key
- Optimistic / pessimistic locking strategy

### 4.3 Network / Timeout
- Recommended client timeout
- Server-side timeout

### 4.4 Invalid Input
- Handling: wrong type, extra fields, null, undefined

### 4.5 Auth / Permission Errors
- Behavior for: expired token, insufficient scope

## 5. Acceptance Criteria

### AC-001: Successful Creation
- **Given** a valid token and correct body
- **When** POST /resources
- **Then** return 201 with id in response

### AC-002: Validation Error
- **Given** name is empty
- **When** POST /resources
- **Then** return 400 with `validation_error`

## 6. Dependencies
- External services: {third-party APIs consumed}
- Internal services: {dependent internal microservices}

## 7. Risks / Open Questions

## 8. Change History
| Date | Change | Author |
```