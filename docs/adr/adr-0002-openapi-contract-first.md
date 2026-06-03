---
title: "ADR-0002: OpenAPI Contract as Source of Truth"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "openapi", "contract", "api"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

このサービスは認証なしの ToDo CRUD API であり、`docs/spec/openapi.yaml` に既に契約が定義されている。実装の自由度を高くしすぎると、クライアント視点での期待値とサーバ実装がずれやすい。

- **CTX-001**: API の正しい振る舞いは、まず仕様書と一致している必要がある。
- **CTX-002**: FastAPI は自動で OpenAPI を生成できるが、生成結果をそのまま正とすると、細かなレスポンス定義やヘッダー定義が仕様とずれる可能性がある。
- **CTX-003**: 本サービスでは、契約の一貫性を優先し、実装と仕様の差分を継続的に検出したい。

## Decision

`docs/spec/openapi.yaml` を API 契約の正とし、FastAPI 実装はこの仕様に合わせる。実装後に生成 OpenAPI を比較し、`operationId`、ステータスコード、`Location` ヘッダー、`Error` schema などの差分を検証する。

- **DEC-001**: 仕様書を契約の唯一の基準として扱う。
- **DEC-002**: FastAPI の自動生成結果は、契約検証の入力として利用する。
- **DEC-003**: 実装は仕様に合わせる側に寄せ、仕様を実装都合で書き換えない。

この方針により、クライアント、バックエンド、テストの期待値を揃えやすくなる。特に `operationId` とエラー形式の固定は、後続の統合テストやクライアント生成でのぶれを減らす。

## Consequences

### Positive

- **POS-001**: API の契約が明確になり、実装・テスト・クライアント生成の基準が一致する。
- **POS-002**: 仕様との差分を早期に検出でき、破壊的変更を抑えやすい。
- **POS-003**: レスポンスやヘッダーの細部まで固定できるため、受け入れテストを書きやすい。
- **POS-004**: ドキュメントと実装の乖離を減らせる。

### Negative

- **NEG-001**: 仕様に合わせるため、FastAPI のデフォルト挙動をそのまま使えない箇所が出る。
- **NEG-002**: OpenAPI 比較の仕組みを維持する運用コストが増える。
- **NEG-003**: 仕様が誤っていた場合でも、実装は一時的に誤仕様へ追随するリスクがある。

## Alternatives Considered

### FastAPI 生成 OpenAPI を正とする

- **ALT-001**: **説明**: 実装を起点に仕様を自動生成し、その内容を契約として公開する。
- **ALT-002**: **不採用理由**: 仕様の意図と自動生成結果が完全一致する保証がなく、エラー形式やヘッダーの表現がぶれやすい。

### 仕様書を用意せず実装先行にする

- **ALT-003**: **説明**: 実装を先に進め、必要になった時点で OpenAPI を整備する。
- **ALT-004**: **不採用理由**: 小規模でも API 契約のぶれが起きやすく、後から整えるとテストとクライアントに追加コストがかかる。

### 何もしない

- **ALT-005**: **説明**: 仕様差分を明示的に管理せず、FastAPI の標準出力に任せる。
- **ALT-006**: **不採用理由**: 契約の安定性を損ない、今回のサービスで重視している再現性と検証可能性を満たせない。

## Implementation Notes

- **IMP-001**: 実装時は、各エンドポイントの `operationId` とレスポンス定義を仕様に合わせて明示する。
- **IMP-002**: CI では生成 OpenAPI と `docs/spec/openapi.yaml` の差分検証を行う。
- **IMP-003**: 仕様を更新する場合は、実装とテストを同時に更新してから差分検証する。
- **IMP-004**: 仕様変更の影響範囲を限定するため、契約を読み込むテストを分離しておく。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0006: Error Handling and Response Normalization
- **REF-003**: ADR-0004: Todo API Behavior and Pagination Rules
