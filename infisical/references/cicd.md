# CI/CD

Primary path for pipelines. Prefer **OIDC** for GitHub Actions; use **Universal Auth** for generic runners.

Confirm action versions and claim formats against:

- https://infisical.com/docs/integrations/cicd/githubactions
- https://infisical.com/docs/documentation/platform/identities/universal-auth

## Decision

```
CI system?
├─ GitHub Actions → OIDC machine identity + Infisical/secrets-action  ★ preferred
├─ Need secrets already in GitHub Secrets store → Secret Syncs (platform.md)
└─ Other CI (GitLab, Circle, custom) → Universal Auth + CLI export/run
```

## GitHub Actions + OIDC (preferred)

### Infisical side

1. Project → Access Control → Machine Identities → create identity.
2. Remove default Universal Auth if unused; add **OIDC Auth**:
   - OIDC Discovery URL: `https://token.actions.githubusercontent.com`
   - Issuer: `https://token.actions.githubusercontent.com`
   - Subject examples:
     - `repo:OWNER/REPO:ref:refs/heads/main`
     - `repo:OWNER/REPO:environment:production`
     - `repo:OWNER/REPO:*` (broader — avoid if possible)
   - Audiences: e.g. `https://github.com/ORG`
3. Grant identity access to the Infisical project/env needed.
4. Copy **Identity ID** (not a secret; safe in YAML).

Debug claims with `github/actions-oidc-debugger` if Subject/Audience fail.

### Workflow template

Pin `Infisical/secrets-action` to the current docs version when possible.

```yaml
name: Deploy

on:
  push:
    branches: [main]

permissions:
  id-token: write   # required for OIDC
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fetch secrets from Infisical
        uses: Infisical/secrets-action@v1.0.9
        with:
          method: oidc
          identity-id: "<identity-id>"
          project-slug: "<project-slug>"
          env-slug: "staging"
          # domain: "https://eu.infisical.com"   # if not US Cloud
          # secret-path: "/apps/api"             # if using folders

      - name: Build
        run: npm ci && npm run build
```

Secrets become **job env vars** after the action step. Do not print values.

### OIDC troubleshooting

| Symptom | Check |
|---------|--------|
| Auth failure | `permissions.id-token: write` present |
| Auth failure | Subject matches repo/ref/environment |
| Auth failure | Audience matches org URL |
| Empty/missing secrets | Identity role on project; `project-slug` / `env-slug` exact |
| Wrong instance | Pass `domain` / EU or self-hosted URL |

## Universal Auth (generic CI / CLI)

Use when OIDC is unavailable.

1. Create machine identity with **Universal Auth**.
2. Store **Client ID** + **Client Secret** in the CI secret store (not in git).
3. Exchange for token, then run/export:

```bash
export INFISICAL_DOMAIN="https://app.infisical.com"   # or EU/self-hosted

export INFISICAL_TOKEN=$(infisical login \
  --method=universal-auth \
  --client-id="$INFISICAL_UNIVERSAL_AUTH_CLIENT_ID" \
  --client-secret="$INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET" \
  --silent --plain)

infisical run --env=staging -- npm run build
# or
infisical export --env=staging --format=dotenv-export > .env
```

CLI also accepts `INFISICAL_UNIVERSAL_AUTH_CLIENT_ID` / `INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET` env vars for the login flags.

Token lifetime is limited — obtain per job, do not reuse long-term.

### Example GitHub Actions with Universal Auth (fallback)

```yaml
permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Infisical CLI
        run: npm install -g @infisical/cli
        # Or follow current distro packages at https://infisical.com/docs/cli/overview
        # (Linux apt/yum repos moved to artifacts-cli.infisical.com; do not copy stale Cloudsmith URLs)

      - name: Auth + run
        env:
          INFISICAL_UNIVERSAL_AUTH_CLIENT_ID: ${{ secrets.INFISICAL_CLIENT_ID }}
          INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET: ${{ secrets.INFISICAL_CLIENT_SECRET }}
        run: |
          export INFISICAL_TOKEN=$(infisical login --method=universal-auth --silent --plain)
          infisical run --env=staging -- npm run build
```

Prefer OIDC over this pattern on GitHub.

## Alternative: sync to GitHub Secrets

If the org wants secrets materialised as GitHub Actions secrets (org/repo/environment), use **GitHub Secret Syncs** instead of runtime fetch — see `platform.md`. Runtime OIDC fetch keeps a single source of truth in Infisical.

## Verify

- [ ] Job authenticates without long-lived Infisical user credentials
- [ ] Required env vars present in subsequent steps
- [ ] Identity scoped to one project/env (least privilege)
- [ ] No secret values in logs or committed workflow artifacts
