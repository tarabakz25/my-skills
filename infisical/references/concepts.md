# Concepts

Vocabulary shared across setup, CI/CD, CLI, and SDK contexts. Load when terms are unclear.

## Core model

| Concept | Meaning |
|---------|---------|
| **Organization** | Top-level Infisical tenant |
| **Project** | App/team secrets container; identified by **project ID** and **project slug** |
| **Environment** | Slice inside a project (`dev`, `staging`, `prod`, or custom **env slug**) |
| **Folder / path** | Path namespace under an env (e.g. `/apps/api`) — CLI `--path` |
| **Secret** | Key/value (optionally versioned) in an env + path |
| **Machine identity** | Non-human principal (CI, server, SDK) with auth methods + project roles |
| **Universal Auth** | Client ID + Client Secret → short-lived access token |
| **OIDC Auth** | Federated login (e.g. GitHub Actions) → short-lived access token |
| **Access token** | Short-lived; often set as `INFISICAL_TOKEN` for CLI |

## Auth choice

| Context | Preferred auth |
|---------|----------------|
| Local developer | Interactive `infisical login` (user) |
| GitHub Actions | OIDC machine identity |
| Generic CI / scripts | Universal Auth → `INFISICAL_TOKEN` |
| App runtime (SDK) | Universal Auth or cloud-native auth (AWS/GCP/Azure/K8s) |
| Cloud-provider workload | Provider auth (AWS IAM, etc.) when available |

## Domain / instance

| Instance | Typical host |
|----------|----------------|
| US Cloud | `https://app.infisical.com` (CLI default) |
| EU Cloud | `https://eu.infisical.com` |
| Self-hosted | Custom URL |

Configure via `INFISICAL_DOMAIN`, `--domain`, or `.infisical.json` `domain`. Precedence: `--domain` > `INFISICAL_DOMAIN` > `.infisical.json` > default. Legacy `INFISICAL_API_URL` still works; `INFISICAL_DOMAIN` wins if both set.

## Delivery modes

1. **Inject at process start** — `infisical run -- cmd` (local/CI with CLI)
2. **Export to file** — `infisical export` (bootstrap only; avoid committing)
3. **Fetch in CI action** — secrets as job env vars (GitHub `secrets-action`)
4. **Fetch in app** — SDK `listSecrets` / `getSecret`
5. **Push outbound** — Secret Syncs (GitHub Secrets, Vercel, AWS, etc.)

## Docs

- Machine identities: https://infisical.com/docs/documentation/platform/identities/machine-identities
- Universal Auth: https://infisical.com/docs/documentation/platform/identities/universal-auth
- Secrets management overview: https://infisical.com/docs/documentation/platform/secrets-mgmt/overview
