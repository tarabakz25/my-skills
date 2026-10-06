# CLI

Load for command details, domain wiring, and export/run options.

Source of truth: https://infisical.com/docs/cli/usage and command pages under https://infisical.com/docs/cli/commands/

## Install

See https://infisical.com/docs/cli/overview — Homebrew, npm (`@infisical/cli`), apt/yum, Winget. Pin versions in prod images.

## Auth

```bash
infisical login                    # interactive user
infisical login -i                 # no browser (WSL/Codespaces/containers)

# Machine identity → token
export INFISICAL_TOKEN=$(infisical login \
  --method=universal-auth \
  --client-id=<id> \
  --client-secret=<secret> \
  --silent --plain)
```

Pass token via `INFISICAL_TOKEN` or `--token`. User login is for local; machine identity for CI/automation.

## Project bind

```bash
infisical init    # .infisical.json (commit)
```

## Common commands

```bash
# Inject into a child process
infisical run --env=dev --path=/apps/api -- npm run dev
infisical run --env=prod --command="source custom.sh && yd"

# List / manage
infisical secrets --env=dev
infisical secrets --projectId <id> --env dev

# Export formats
infisical export --format=dotenv-export > .env
infisical export --format=yaml > secrets.yaml

# Scan for leaks
infisical scan --verbose
infisical scan install --pre-commit-hook
```

Exact subcommands evolve — verify with `infisical --help` / docs before scripting unusual flags.

## Domain configuration

Precedence: `--domain` > `INFISICAL_DOMAIN` > `.infisical.json` `domain` > US Cloud default.

```bash
export INFISICAL_DOMAIN="https://eu.infisical.com"
infisical login --method=universal-auth --client-id=... --client-secret=... --silent --plain
```

If you only pass `--domain` on login, later commands still need domain via env, flag, or `.infisical.json`.

## Custom headers

```bash
export INFISICAL_CUSTOM_HEADERS="Access-Client-Id=... Access-Client-Secret=..."
```

## Shell history

Avoid storing `infisical secrets set ...` in history (`HISTIGNORE` pattern for those commands). See CLI usage FAQ.

## Service tokens (legacy)

Still accepted as `--token` / `INFISICAL_TOKEN` for some flows; prefer **machine identities** (Universal Auth / OIDC) for new automation.
