# Driver adapters / Accelerate (Prisma v7)

## いつ必要？

- `schema.prisma` の `generator client { provider = "prisma-client" }`（新クライアント）を使う場合、`new PrismaClient({ adapter })` か `new PrismaClient({ accelerateUrl })` が必要になることが多い。
- 既存の `new PrismaClient()` を保ちたい場合は、まず `provider = "prisma-client-js"`（legacy）を選ぶのが安全。

## PostgreSQL + `@prisma/adapter-pg`（例）

依存追加（例）:
- `npm i @prisma/adapter-pg pg`

クライアント初期化（例）:

```ts
import "dotenv/config";
import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
});

export const prisma = new PrismaClient({ adapter });
```

メモ:
- driver adapter を使う場合、接続文字列は **schema.prisma からは読まれず**、コード側で渡す。

## Prisma Accelerate（考え方だけ）

- DB 直結ではなく Accelerate 経由にしたい場合、`accelerateUrl` を環境変数で渡して `PrismaClient` を初期化する。
- 具体例は Prisma の設定（プラン/環境）に強く依存するので、まず要件（本番の接続方式、Vercel/Cloudflare Workers など）を確認してから実装する。

