---
title: "ADR-0005: Date and Time Conventions"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "datetime", "timezone", "serialization"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

ToDo には期限日と作成・更新日時があり、ここを曖昧にすると比較・表示・保存の各段階で不整合が起きやすい。特に API では、日付と日時の型を混ぜるとクライアント実装の難度が上がる。

- **CTX-001**: `dueDate` は日付のみで、タイムゾーンを持たない。
- **CTX-002**: `createdAt` と `updatedAt` は実際の発生時刻として扱う必要がある。
- **CTX-003**: JSON シリアライズ時の表現は一貫している必要がある。

## Decision

`dueDate` は timezone を持たない `date` とし、`createdAt` と `updatedAt` は UTC の timezone-aware `datetime` とする。DB 保存時も UTC に統一し、JSON では ISO 8601 形式で返す。

- **DEC-001**: `dueDate` は日付のみを表す。
- **DEC-002**: `createdAt` / `updatedAt` は UTC で保存する。
- **DEC-003**: API レスポンスでは ISO 8601 形式を返す。
- **DEC-004**: サーバ内部ではローカル時刻に依存しない。

この方針により、期限日と監査系時刻の意味を分離できる。日付の比較とタイムゾーン計算を分けて扱えるため、クライアント側の実装も単純になる。

## Consequences

### Positive

- **POS-001**: `dueDate` と日時の役割が明確に分かれ、扱いを誤りにくい。
- **POS-002**: UTC 統一により、環境差による時刻ずれを防ぎやすい。
- **POS-003**: ISO 8601 での返却により、クライアントとの相互運用性が高い。
- **POS-004**: 比較・ソート・テストが安定しやすい。

### Negative

- **NEG-001**: UTC 変換の扱いを誤ると、境界時刻で混乱が起きる。
- **NEG-002**: ローカルタイム前提の UI では、表示時に変換処理が必要になる。
- **NEG-003**: 日付と日時の型差を実装全体で維持する必要がある。

## Alternatives Considered

### すべてを日時に統一する

- **ALT-001**: **説明**: `dueDate` も日時として扱い、タイムゾーン付きで保存する。
- **ALT-002**: **不採用理由**: 期限日は日付だけで十分であり、不要なタイムゾーン複雑性を増やす。

### ローカルタイムで保存する

- **ALT-003**: **説明**: サーバのローカル時刻をそのまま保存・返却する。
- **ALT-004**: **不採用理由**: 実行環境差で結果が変わり、再現性と比較可能性が落ちる。

### 文字列として曖昧に扱う

- **ALT-005**: **説明**: 日付と日時を文字列のまま運び、厳密な型を持たせない。
- **ALT-006**: **不採用理由**: 入力検証とシリアライズの責務が不明確になり、バグを招きやすい。

## Implementation Notes

- **IMP-001**: 保存前に UTC に正規化し、返却時も同一表現に揃える。
- **IMP-002**: `dueDate` のバリデーションは日付専用として扱い、日時パースと混在させない。
- **IMP-003**: テストではタイムゾーンを固定し、時刻が揺れないようにする。
- **IMP-004**: サーバ時刻の取得箇所を集約して、差し替え可能にしておく。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0004: Todo API Behavior and Pagination Rules
- **REF-003**: ADR-0006: Error Handling and Response Normalization
