# Troubleshooting (Prisma v7)

## `We have detected that your project does not have a prisma.config.ts file...`

原因:
- v7 では migrate / introspect（`migrate dev`, `migrate deploy`, `db pull`, `db push` など）に `prisma.config.ts` が必須。

対処:
- `npx prisma init` で雛形を作る、または `references/templates.md` をベースに手動で `prisma.config.ts` を追加する。
- `schema` と `migrations.path` がプロジェクト構成と一致しているか確認する。

## `The datasource property url is no longer supported in Prisma v7`

原因:
- v6 まで `schema.prisma` の `datasource db { url = env("DATABASE_URL") }` を使っていた。
- v7 では `datasource.url`（接続先）は `prisma.config.ts` で定義する。

対処:
- `schema.prisma` の `datasource` から `url` / `directUrl` を削除する（`provider` だけ残す）。
- `prisma.config.ts` に `datasource: { url: process.env["DATABASE_URL"] }` を追加する（テンプレは `references/templates.md`）。

## `P1012 Environment variable not found: DATABASE_URL` / `DATABASE_URL is not set`

原因:
- Prisma v7 の CLI は `.env` を自動ロードしないため、`process.env.DATABASE_URL` が空のまま。

対処:
- ローカル開発なら `prisma.config.ts` に `import "dotenv/config"` を追加する。
- もしくは `dotenv-cli` 等で `dotenv -- prisma ...` の形にする。
- CI/本番では環境変数として `DATABASE_URL` を注入する（.env 前提にしない）。

## `PrismaClient requires either the adapter option or the accelerateUrl option`

原因（典型）:
- `generator client { provider = "prisma-client" }`（新クライアント）を使っているのに、`new PrismaClient()` のまま。

対処:
- driver adapter を使う（`references/adapters.md`）。
- もしくは `schema.prisma` の generator を `prisma-client-js`（legacy）に戻して、まず動作優先で通す。

## `MongoDB is no longer supported in Prisma ORM v7`

対処:
- MongoDB を使うプロジェクトは Prisma v6 系を維持する（当面 v7 へ上げない）。

