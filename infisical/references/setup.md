# Setup (repo + local)

Primary path when adding Infisical to a project for local development.

Fetch latest install/flags from https://infisical.com/docs/cli/overview and https://infisical.com/docs/cli/usage when versions matter.

## Checklist

1. [ ] Choose instance (US / EU / self-hosted) and domain config
2. [ ] Install CLI
3. [ ] Create or select Infisical project + environments
4. [ ] `infisical login` (interactive)
5. [ ] `infisical init` → commit `.infisical.json`
6. [ ] Store secrets in Infisical (not in git)
7. [ ] Wire `infisical run` into npm/make scripts
8. [ ] Document required keys for the team (names only)
9. [ ] Optional: add CI (see `cicd.md`)

## Install CLI

```bash
# macOS
brew install infisical/get-cli/infisical

# npm (any OS)
npm install -g @infisical/cli
```

Pin CLI version in production/CI images when reproducibility matters.

## Login + init

```bash
infisical login          # browser; use -i in WSL/Codespaces/containers
cd /path/to/repo
infisical init           # writes .infisical.json — safe to commit
```

Example `.infisical.json` fields:

```json
{
  "workspaceId": "<project-id>",
  "defaultEnvironment": "dev",
  "domain": "https://eu.infisical.com"
}
```

Omit `domain` for US Cloud default. Only set `domain` to a trusted host (committed file triggers a CLI warning).

## Inject secrets locally

```bash
infisical run --env=dev --path=/apps/api -- npm run dev
infisical run --env=staging -- nodemon index.js
```

Prefer `run` over committing `.env`. If a tool requires a file:

```bash
infisical export --env=dev --format=dotenv-export > .env
# ensure .env is gitignored
```

## package.json pattern

```json
{
  "scripts": {
    "dev": "infisical run --env=dev -- next dev",
    "start": "infisical run --env=prod -- node server.js"
  }
}
```

Document that contributors need CLI + login (or a shared machine identity for containers).

## Migrating from `.env` / other vaults

1. Inventory keys in existing `.env*` / Doppler / Vault.
2. Create matching Infisical env + path structure.
3. Upload values via UI/CLI (`infisical secrets set` — avoid leaving values in shell history; configure `HISTIGNORE` for `infisical secrets set`).
4. Switch scripts to `infisical run`.
5. Remove committed secret files; keep `.env.example` with empty/placeholder values only.
6. Add CI next (`cicd.md`).

## Self-hosted / EU notes

```bash
export INFISICAL_DOMAIN="https://eu.infisical.com"
# or self-hosted URL
infisical login
```

For proxies (e.g. Cloudflare Access):

```bash
export INFISICAL_CUSTOM_HEADERS="Access-Client-Id=... Access-Client-Secret=..."
```

## Verify

```bash
infisical secrets --env=dev
infisical run --env=dev -- printenv | grep -E '^(DATABASE_|API_)'   # names only; avoid dumping all
```

Confirm `.infisical.json` is tracked and `.env` / credentials are not.
