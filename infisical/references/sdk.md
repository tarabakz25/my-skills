# SDK

Load when the **application** should fetch secrets at runtime (not only CLI inject).

Overview: https://infisical.com/docs/sdks/overview  
Languages: Node, Python, Go, Java, .NET, Ruby, PHP, Rust, C++ — open language-specific docs from the overview when implementing.

## When to use SDK vs CLI

| Need | Prefer |
|------|--------|
| Local/dev process env injection | CLI `infisical run` |
| CI job env | CI action / CLI (`cicd.md`) |
| App reads secrets dynamically / rotates without redeploy | SDK |
| Edge/serverless with provider identity | SDK + cloud auth when available |

## Node.js (representative)

Docs: https://infisical.com/docs/sdks/languages/node  
Package: `@infisical/sdk` — Node **20+** for SDK v5+.

```typescript
import { InfisicalSDK } from "@infisical/sdk";

const client = new InfisicalSDK({
  // siteUrl optional; default https://app.infisical.com
  siteUrl: process.env.INFISICAL_DOMAIN, // e.g. https://eu.infisical.com
});

await client.auth().universalAuth.login({
  clientId: process.env.INFISICAL_CLIENT_ID!,
  clientSecret: process.env.INFISICAL_CLIENT_SECRET!,
});

const { secrets } = await client.secrets().listSecrets({
  environment: "prod",
  projectId: process.env.INFISICAL_PROJECT_ID!,
  secretPath: "/apps/api",
  expandSecretReferences: true,
});
```

Other auth methods exist (AWS IAM, etc.) — use when running inside that cloud.

### Patterns

- Store **Client ID/Secret** (or cloud role) via platform secrets / prior CLI inject — avoid hardcoding.
- Cache: SDKs typically cache secrets and fall back to cache / `process.env` on failure (confirm per language FAQ).
- Prefer listing by path + env; request least privilege on the machine identity.
- Do not log secret values.

## Python / Go / others

Follow the language page from the SDK overview. Flow is the same: create client → authenticate (Universal Auth or native) → `list`/`get` secrets for `project` + `environment` (+ path).

## Verify

- [ ] Machine identity can read only required project/env/path
- [ ] `siteUrl`/domain matches instance
- [ ] Failure mode tested (cache / env fallback) for production readiness
- [ ] No secrets in source or client bundles
