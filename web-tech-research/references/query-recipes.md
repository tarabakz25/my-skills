# Query recipes

目的: ユーザーの質問を「検索クエリのセット」に落とし込む。

## 基本の型

- `<product> release notes` / `<product> changelog` / `<product> GitHub releases`
- `<product> breaking changes` / `<product> migration guide` / `<product> upgrade guide`
- `<product> deprecation` / `<product> EOL` / `<product> support policy` / `<product> lifecycle`
- `<product> pricing` / `<product> pricing changes`
- `<product> security advisory` / `<product> CVE` / `<product> vulnerability`
- `<product> <version> compatibility <runtime>`（例: `python 3.13`, `node 22`, `kubernetes 1.30`）

## まず広く当てる（1 本）

- 例: `<product> latest version release date`
- 目的: 「何を調べるべきか」を把握し、公式出典のあたりを付ける

## 次に公式で確証する（1〜2 本）

優先候補（分かる範囲で）:

- 公式ドキュメント（`docs.*`, `developer.*`）
- 公式ブログ（`blog.*`）
- 公式リポジトリ（`github.com/<org>/<repo>`）の Releases / Tags / CHANGELOG
- 公式パッケージレジストリ（npm/PyPI/Maven Central/NuGet 等）

## 深掘り（必要なときだけ 1 本）

- breaking が疑われる: `<product> breaking changes <major version>`
- 移行が必要: `<product> migration guide <from> <to>`
- セキュリティ: `<product> security advisory` + `CVE-YYYY`
- 価格/プラン: `<product> pricing` + `effective` / `announced` / `change`

## 言い換え（ヒットしないとき）

- “release notes” ↔ “what’s new” ↔ “announcements”
- “upgrade guide” ↔ “migration” ↔ “porting”
- “support policy” ↔ “lifecycle” ↔ “EOL” ↔ “end of support”

