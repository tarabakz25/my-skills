# Platform

Secondary contexts: outbound syncs, scanning, rotation, dynamic secrets. Keep setup/CI primary; load this when the user asks for these features.

Prefer docs index: https://infisical.com/docs/llms.txt

## Secret Syncs

Push Infisical secrets to external systems (GitHub Secrets, Vercel, AWS, etc.).

- Use when consumers expect native platform secrets (e.g. GitHub repo secrets) rather than runtime fetch.
- For GitHub Actions runtime injection without syncing, prefer OIDC + `secrets-action` (`cicd.md`).
- Configure connection + sync in Infisical UI/API; do not duplicate sync logic in app code.

GitHub syncs docs: search “GitHub Secret Syncs” under Infisical integrations.

## Secret scanning

```bash
infisical scan --verbose
infisical scan install --pre-commit-hook
```

Use to prevent committing credentials. Pair with `.env` gitignore and setup migration checklist.

## Rotation & dynamic secrets

- **Rotation**: scheduled credential replacement for supported integrations.
- **Dynamic secrets**: short-lived leased credentials.

Use when static long-lived DB/cloud keys are unacceptable. Implementation is provider-specific — open current Infisical docs for the target system before coding.

## Folders, imports, approvals

- **Folders/paths**: scope CLI `--path` / SDK `secretPath`.
- **Imports**: share secret sets across envs/projects (env-local wins on conflict — confirm in current docs).
- **Approvals / PIT recovery**: governance features for sensitive envs — configure in platform, not in app repos.

## PKI / PAM / extras

Infisical also covers certificates and privileged access. Out of scope for default secrets setup/CI unless the user explicitly asks — fetch dedicated docs then.
