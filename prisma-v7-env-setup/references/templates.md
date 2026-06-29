# Templates

## `prisma.config.ts` (minimal)

```ts
import "dotenv/config";
import { defineConfig } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: {
    url: process.env["DATABASE_URL"],
  },
});
```

メモ:
- Prisma v7 の CLI は `.env` を自動ロードしないため、ローカル開発では `import "dotenv/config"` を入れておくのが安全。
- `.env` を読ませたくない環境（本番/CI）では、プロセス環境変数として `DATABASE_URL` を注入する。

## `prisma/schema.prisma` (Postgres + legacy client 例)

最小変更で通したい場合（`new PrismaClient()` を保ちたい）:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
}

model User {
  id    String @id @default(cuid())
  email String @unique
}
```

## `prisma/schema.prisma` (new client 例)

新クライアントを選ぶ場合（driver adapter / Accelerate の準備が必要）:

```prisma
generator client {
  provider = "prisma-client"
}

datasource db {
  provider = "postgresql"
}
```

## `package.json` scripts (例)

```jsonc
{
  "scripts": {
    "postinstall": "prisma generate",
    "db:validate": "prisma validate",
    "db:migrate:dev": "prisma migrate dev",
    "db:migrate:deploy": "prisma migrate deploy",
    "db:studio": "prisma studio"
  }
}
```

