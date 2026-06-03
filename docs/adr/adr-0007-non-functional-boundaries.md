---
title: "ADR-0007: Non-Functional Boundaries and Operational Baseline"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "operations", "healthcheck", "logging", "cors", "settings"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

機能がシンプルでも、運用上の最低限の境界は必要である。CORS、ヘルスチェック、ログ、設定管理、認証境界を明確にしないと、後から足すときに責務が混ざりやすい。

- **CTX-001**: この段階では外部フロントエンドとの統合前提を置かない。
- **CTX-002**: サービスの生死確認は、実装本体と切り離した方がよい。
- **CTX-003**: 設定値はコードに埋め込まず、環境変数で注入したい。

## Decision

CORS は不要とし、`GET /healthz` を追加する。ログは文字列形式で出力し、設定管理には `pydantic-settings` を使う。認証認可は実装しないが、将来の拡張を妨げないように middleware 境界は意識して実装する。

- **DEC-001**: CORS は無効のままとする。
- **DEC-002**: `GET /healthz` を提供する。
- **DEC-003**: ログは文字列ベースで出力する。
- **DEC-004**: 設定は `pydantic-settings` で環境変数から読む。
- **DEC-005**: 認証認可は現時点では実装しない。

この決定により、最小限の運用確認手段を持ちながら、不要な境界拡大を避けられる。`healthz` と設定管理を分離しておくことで、将来のデプロイ先変更や監視追加にも対応しやすい。

## Consequences

### Positive

- **POS-001**: `healthz` により、疎通確認と監視の入り口ができる。
- **POS-002**: 環境変数ベースの設定で、デプロイ差分をコードから切り離せる。
- **POS-003**: CORS を入れないことで、不要な設定と誤解を減らせる。
- **POS-004**: 認証境界を明示しておくことで、将来追加時の影響範囲を把握しやすい。

### Negative

- **NEG-001**: CORS を不要とするため、ブラウザ直接接続の要件が出た場合は追加対応が必要になる。
- **NEG-002**: 文字列ログのみでは、構造化分析や相関追跡が弱い。
- **NEG-003**: 認証を後付けする際は、middleware とルーティングの再調整が必要になる。
- **NEG-004**: `healthz` を追加することで、仕様外エンドポイントの管理が増える。

## Alternatives Considered

### CORS を許可する

- **ALT-001**: **説明**: フロントエンド接続を見越して、あらかじめ origin を許可する。
- **ALT-002**: **不採用理由**: 現時点では不要であり、誤った広い許可設定を招きやすい。

### 構造化ログを先に導入する

- **ALT-003**: **説明**: JSON 形式などでログを出し、検索や相関分析をしやすくする。
- **ALT-004**: **不採用理由**: 現段階では過剰で、実装と運用の複雑さが増える。

### 認証認可を同時に実装する

- **ALT-005**: **説明**: 今のうちに middleware も含めて認証を入れる。
- **ALT-006**: **不採用理由**: 仕様に反し、学習用の小規模 API としてのシンプルさを損なう。

## Implementation Notes

- **IMP-001**: `GET /healthz` は外部依存を持たない軽量な応答にする。
- **IMP-002**: 設定クラスを一箇所に集約し、環境変数の一覧を把握しやすくする。
- **IMP-003**: ログは最低限の追跡に使えるよう、リクエスト単位の文脈を将来追加しやすい形にしておく。
- **IMP-004**: 認証を追加する場合は、ルートハンドラではなく middleware / dependency で差し込める構造にする。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0002: OpenAPI Contract as Source of Truth
- **REF-003**: ADR-0006: Error Handling and Response Normalization
