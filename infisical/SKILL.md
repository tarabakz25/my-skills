---
name: infisical
description: >-
  Full-stack Infisical secrets workflows: repo setup (CLI install, login, init,
  .infisical.json, run/export), CI/CD (GitHub Actions OIDC, Universal Auth machine
  identities), CLI ops, SDK integration (Node/Python/etc.), and platform features
  (syncs, scan, rotation). Use when setting up Infisical, wiring secrets into local
  dev or CI/CD, injecting/exporting secrets, integrating Infisical SDKs, migrating
  from .env/Doppler/Vault, or configuring machine identities / secret syncs.
  Prefer Infisical docs over baked-in knowledge.
disable-model-invocation: true
metadata:
  hermes:
    tags:
      - infisical
      - secrets
      - env
      - cli
      - cicd
      - github-actions
      - oidc
      - sdk
      - machine-identity
    related_skills: [prisma-v7-env-setup, init, web-perf]
---

# Infisical

## Overview

Infisical centralizes secrets (API keys, DB creds, config) and delivers them via CLI, SDKs, CI actions, and syncs. This skill is **full-stack** but **context-separated** — load only the reference for the current task.

Prefer live docs over this skill when citing flags, action versions, or API shapes:

| Source | URL |
|--------|-----|
| Docs index | https://infisical.com/docs/llms.txt |
| CLI quickstart | https://infisical.com/docs/cli/usage |
| GitHub Actions | https://infisical.com/docs/integrations/cicd/githubactions |
| SDKs | https://infisical.com/docs/sdks/overview |
| Machine identities | https://infisical.com/docs/documentation/platform/identities/machine-identities |

## Context router

```
Task?
├─ New/existing repo → Infisical for local+team  → references/setup.md   ★ primary
├─ GitHub Actions / other CI                      → references/cicd.md    ★ primary
├─ CLI commands, domain, export/run details       → references/cli.md
├─ App fetches secrets at runtime (SDK)           → references/sdk.md
├─ Syncs / scan / rotation / folders              → references/platform.md
└─ Projects, envs, paths, identities (vocab)      → references/concepts.md
```

**Default bias:** if the user asks to “add Infisical” without specifying runtime SDK fetch, do **setup** first, then **CI/CD** if a pipeline exists.

## Primary workflow A — Setup (local repo)

1. Confirm instance: US Cloud (`app.infisical.com`), EU (`eu.infisical.com`), or self-hosted → set `INFISICAL_DOMAIN` / `.infisical.json` `domain` when not US.
2. Install CLI → `infisical login` (use `-i` in containers/WSL/Codespaces).
3. `infisical init` in repo root → commit `.infisical.json` (no secrets).
4. Map envs (`dev`/`staging`/`prod`) and optional `--path=/...`.
5. Wire package scripts to `infisical run --env=... -- <cmd>`.
6. Keep real secrets out of git; `.env` only as exported/local artifact if needed.

Load `references/setup.md` for the full checklist.

## Primary workflow B — CI/CD

Prefer **OIDC machine identity** for GitHub Actions (no long-lived client secret in GitHub).

1. Create machine identity → OIDC Auth (Discovery/Issuer: `https://token.actions.githubusercontent.com`).
2. Restrict Subject/Audience (repo + context); copy **Identity ID** (safe to commit).
3. Grant project access for the target env.
4. Workflow: `permissions: id-token: write` + `Infisical/secrets-action` with `method: oidc`.
5. Fallback for generic CI: Universal Auth → `INFISICAL_TOKEN` via `infisical login --method=universal-auth ... --silent --plain`.

Load `references/cicd.md` for templates and troubleshooting.

## Safety rules

- Never commit client secrets, access tokens, or exported `.env` with real values.
- Do not `echo` secret values in CI logs.
- Prefer OIDC over Universal Auth in GitHub Actions when possible.
- Identity ID / project slug / env slug are not secrets; client secrets are.
- Service tokens are legacy for non-local use; prefer machine identities.

## Common pitfalls

- Missing `id-token: write` → OIDC auth fails.
- Subject/Audience mismatch on machine identity vs workflow claims.
- Wrong `env-slug` / `project-slug` (case-sensitive).
- EU/self-hosted without `INFISICAL_DOMAIN` / `--domain` / `.infisical.json` domain.
- Using interactive browser login in CI (use Universal Auth or OIDC).

## Verification checklist

- [ ] `.infisical.json` present and committed; no secrets in git
- [ ] Local: `infisical run --env=dev -- <app>` injects expected keys
- [ ] CI: workflow authenticates (OIDC or Universal Auth) and job sees secrets as env vars
- [ ] Machine identity scoped to least-privilege project/env
- [ ] Domain correct for Cloud region / self-hosted instance

## Resources

- `references/setup.md` — install, login, init, local inject
- `references/cicd.md` — GitHub Actions OIDC + Universal Auth CI
- `references/cli.md` — CLI commands and domain config
- `references/sdk.md` — language SDKs
- `references/platform.md` — syncs, scan, rotation
- `references/concepts.md` — model vocabulary
