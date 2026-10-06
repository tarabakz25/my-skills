---
name: prisma-v7-env-setup
description: >-
  Set up or upgrade Prisma ORM v7 in Node.js/Next.js projects (install prisma +
  @prisma/client, create prisma.config.ts, configure datasource URL, handle Prisma CLI
  .env loading changes, run generate/migrate/introspect/studio, and fix common Prisma v7
  errors). Use when doing Prisma v7 setup, upgrade, init, config, or error fixes (Prisma
  v7の環境構築・アップグレード・初期化・設定・エラー解消).
disable-model-invocation: true
---

# Prisma V7 Env Setup

## Overview

Prisma ORM v7 の「環境構築（依存追加・設定ファイル・DB接続・マイグレーション）」を、プロジェクトの状況（新規/既存、CJS/ESM、adapter利用/非利用）に合わせて最短で通す。

## Workflow Decision Tree

1. **新規導入**: `package.json` に Prisma が無い → 「New project」へ
2. **既存から v7 へ移行**: v6 以前 → 「Upgrade existing project」へ
3. **CLI が動かない/エラーが出る**: → 「Troubleshooting」へ
4. **Prisma Client をどうしたいか**
   - **既存コードを最小変更**（`new PrismaClient()` で動かしたい）→ `generator client { provider = "prisma-client-js" }` を優先
   - **新しいクライアント（Rust-free/ESM 既定）**を使う → `provider = "prisma-client"` を使い、**driver adapter or Accelerate** を設定（`references/adapters.md`）

## Step 0: Prerequisites (必須)

- **Node.js**: Prisma v7 は Node の最小バージョン制約が厳しめ。まず `node -v` を確認し、サポート対象へ上げる。
- **パッケージマネージャ**: npm/pnpm/yarn/bun いずれでもよいが、CI と揃える。
- **DB**: Postgres/MySQL/SQLite など使用 DB を決める（MongoDB は v7 非対応になったので注意）。

迷ったら最初に `scripts/prisma7-doctor.mjs` を実行して、プロジェクトの状態と次アクションを機械的に確認する。

## New Project (Prisma v7 を新規導入)

### 1) 依存追加

- `prisma`（CLI）は devDependencies、`@prisma/client` は dependencies に入れる。
- 例（npm）: `npm i @prisma/client && npm i -D prisma`

### 2) Prisma 初期化（`prisma/` と `prisma.config.ts`）

- `npx prisma init` を実行して初期ファイルを作る（既存の構成がある場合は生成結果を採用せず手動調整してOK）。
- v7 では **`prisma.config.ts` が migrate/introspect に必須**。テンプレは `references/templates.md`。

### 3) DB 接続設定（重要: v7 は schema.prisma に url を書かない）

- v7 では `datasource db { ... }` から **`url` が無くなり**、`prisma.config.ts` 側で `datasource.url` を設定する。
- 併せて、Prisma CLI は **`.env` を自動ロードしない**ため、`prisma.config.ts` 内で `.env` を読み込む（`references/templates.md`）。

### 4) マイグレーション & 生成

- 開発: `npx prisma migrate dev`
- 反映だけ（本番/CI）: `npx prisma migrate deploy`
- 生成: `npx prisma generate`（`postinstall` に入れるかは運用次第）
- Studio: `npx prisma studio`

## Upgrade Existing Project (v6 以前 → v7)

### 1) 依存を v7 に揃える

- `prisma` と `@prisma/client` を v7 系に揃える（片方だけ上げない）。
- `npx prisma -v` と `node -v` を記録しておく。

### 2) `prisma.config.ts` を追加/移行

- v7 では **`prisma.config.ts` が必要**。無い場合は追加する（テンプレは `references/templates.md`）。
- 旧構成で `schema.prisma` の `datasource.url` / `directUrl` を使っていたら削除し、`prisma.config.ts` の `datasource.url` に移す。
- `prisma` ブロック（`package.json` の Prisma 設定）は v7 で削除対象（あれば `prisma.config.ts` に寄せる）。

### 3) `.env` ロード戦略を決める

- v7 の CLI は `.env` を自動で読まない。以下のどれかに統一する:
  - `prisma.config.ts` で `import "dotenv/config"`（または手書きローダー）
  - `dotenv-cli` 等で `dotenv -- prisma ...` の形にする
  - 実行環境（CI/本番）で `DATABASE_URL` を注入する

### 4) Prisma Client の方針（adapter の要否）

- **最小変更**: `schema.prisma` の generator を `prisma-client-js` のままにすると、既存の `new PrismaClient()` を保ちやすい。
- **新クライアント**: generator を `prisma-client` に変更する場合、**driver adapter か Prisma Accelerate** が必要になることが多い。`references/adapters.md` の例に従い、コード側の初期化も更新する。

## Troubleshooting (よくある v7 詰まりポイント)

詳細は `references/troubleshooting.md` を参照。まずはエラーメッセージをそのまま貼ってもらい、該当箇所を切り分ける。

## Resources

### scripts/
- `scripts/prisma7-doctor.mjs`: 依存/ファイル/設定の自動チェックと次アクション提示

### references/
- `references/templates.md`: `prisma.config.ts` / `schema.prisma` / `package.json` scripts の最小テンプレ
- `references/adapters.md`: `prisma-client`（新クライアント）での driver adapter / Accelerate の手引き
- `references/troubleshooting.md`: v7 移行時の代表的なエラーと対処
