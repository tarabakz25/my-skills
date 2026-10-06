---
name: web-tech-research
description: Retrieve up-to-date technical information using web search for libraries, frameworks, APIs, CLIs, cloud services, security advisories (CVE), pricing, compatibility, deprecations, and release notes. Use when the user asks for 最新/最新情報/調べて/verify/リリースノート/互換性/サポート期限/価格変更, or when the answer may have changed recently.
disable-model-invocation: true
---

# Web Tech Research

目的: ユーザーの入力に対して必要な「最新の技術情報」を Web search で確認し、一次情報中心に短く行動可能な形で返す。

## 1) 先に聞く（不明点があれば最小限）

不足があれば、質問は 1〜3 個に絞る（聞きすぎない）。相対日付（今日/昨日）を避け、必要なら絶対日付で確認する。

- 対象: 製品/OSS/サービス名、URL、現行バージョン
- 観点: 最新バージョン/互換性/Breaking change/移行/価格/セキュリティ/サポート期限
- 環境: 言語/ランタイム/OS/クラウド/制約（例: 企業プロキシ、FIPS、LTS縛り）
- 出典の優先: 公式のみか、英語可か、ブログ/動画可否
- 「最新」の定義: 直近 N 日、現行 LTS、最新安定版、など

不明点が多い場合は、仮定（Assumptions）を明示して進め、ユーザーに確認する。

## 2) 検索戦略（一次情報を最優先）

基本は「広く把握 → 公式で確証 → 深掘り（breaking/security/pricing）」の順に調べる。

- 公式ドキュメント / リリースノート / Changelog / 公式ブログ / GitHub Releases を最優先
- 仕様や標準: RFC / 公式仕様書
- 価格やサポート: 公式 Pricing / Support policy / Lifecycle policy
- セキュリティ: ベンダーアドバイザリ + CVE（NVD / GitHub Security Advisory など）

クエリ作成は `references/query-recipes.md`、情報源の優先順位は `references/source-quality.md` を参照する。

## 3) `web.run` の使い方（推奨）

- `search_query` は 2〜4 本に絞る（多すぎない）
- 時事性が高い場合は `recency` を指定する（例: 7/30/365 日）
- 公式ドメインが分かる場合は `domains` で絞る
- 重要情報（version / breaking / deprecate / pricing / CVE）は `open`/`find` で一次情報の該当箇所まで当てる

## 4) 事実抽出（必ず日付を添える）

- バージョン番号、リリース日、変更点（breaking の有無）
- 互換性・必要条件（最低ランタイム/OS/依存関係）
- 推奨される移行手順（公式ガイドの要点）
- 既知の注意点（Issue/PR/FAQ）。推測は推測と明記する

## 5) 出力（短く、行動可能に）

最低限、以下を満たす。

- 結論（1〜3 行）
- 要点（箇条書き。各項目に日付/バージョンを付ける）
- 影響と次のアクション（ユーザーがやること）
- 不確実性（不足情報、未確定点、追加で確認したい点）
- 出典（引用ハンドルが使える環境なら引用、無いなら URL を `code` で列挙）

