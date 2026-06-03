---
title: "ADR-0006: Error Handling and Response Normalization"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "errors", "validation", "api"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

API エラーは、クライアントが最も扱い方に困る領域の一つである。FastAPI は標準で 422 を返せるが、仕様では `Error` schema に寄せた 400/404/500 系の応答が想定されている。したがって、実装のデフォルト挙動をそのまま公開しない方がよい。

- **CTX-001**: 入力エラーは、クライアントが解釈しやすい共通形式にしたい。
- **CTX-002**: 存在しないリソースは、全エンドポイントで同じ意味と構造で返したい。
- **CTX-003**: 予期しない障害も、最低限の共通エラーとして包みたい。

## Decision

リクエスト validation error は `400 BadRequest` に変換し、レスポンスは `{code, message, details}` に統一する。`404` は `code=not_found` を共通化し、予期しない例外は共通の `500` エラーレスポンスに変換する。

- **DEC-001**: validation error を 400 に変換する。
- **DEC-002**: `Error` schema に合わせて `code`, `message`, `details` を返す。
- **DEC-003**: `404` は `not_found` で統一する。
- **DEC-004**: 未処理例外は共通 500 形式に変換する。

この方針により、FastAPI の内部実装に依存しすぎず、クライアントから見たエラーの形を安定させられる。特に validation と domain error を同じ応答形式に寄せることで、クライアント実装を簡単にできる。

## Consequences

### Positive

- **POS-001**: エラーの形が統一され、クライアント側の分岐が簡単になる。
- **POS-002**: 仕様書と実装のエラー応答が揃いやすい。
- **POS-003**: `details` により、入力エラーのフィードバックが具体的になる。
- **POS-004**: 500 を共通化することで、想定外障害の露出が制御しやすい。

### Negative

- **NEG-001**: FastAPI の標準 422 をそのまま使えず、変換処理が必要になる。
- **NEG-002**: エラーハンドリング用の共通層を維持する必要がある。
- **NEG-003**: 500 を隠すだけでは根本原因は解決しないため、ログ設計が別途必要になる。

## Alternatives Considered

### FastAPI の 422 をそのまま返す

- **ALT-001**: **説明**: フレームワーク標準の validation エラーをそのまま公開する。
- **ALT-002**: **不採用理由**: 仕様の `Error` schema とずれ、クライアント実装が FastAPI に引きずられる。

### すべてのエラーを HTTP ステータスだけで表す

- **ALT-003**: **説明**: ボディは最小限にして、ステータスコードだけで意味を伝える。
- **ALT-004**: **不採用理由**: 入力項目単位の原因が分からず、デバッグ性が落ちる。

### 予期しない例外をそのまま返す

- **ALT-005**: **説明**: 例外をフレームワークの既定応答に任せる。
- **ALT-006**: **不採用理由**: 応答形式がぶれ、API 利用者にとって扱いづらい。

## Implementation Notes

- **IMP-001**: validation error、not found、unexpected error のハンドラを分けて実装する。
- **IMP-002**: `details` は入力項目単位の情報に限定し、冗長な内部情報は返さない。
- **IMP-003**: 500 エラーはクライアントに内部実装詳細を出さず、ログ側に原因を残す。
- **IMP-004**: 仕様にないエラー応答を増やしすぎない。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0002: OpenAPI Contract as Source of Truth
- **REF-003**: ADR-0007: Non-Functional Boundaries and Operational Baseline
