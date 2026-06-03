---
title: "ADR-0004: Todo API Behavior and Pagination Rules"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "api", "behavior", "pagination"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

`docs/spec/openapi.yaml` は CRUD API の基本的な振る舞いを定義しているが、実装時に曖昧さが残るとテスト結果がぶれやすい。特に更新の扱い、一覧の順序、ページング、作成時の初期値は、クライアントから見た安定性に直結する。

- **CTX-001**: `POST` は新規作成であり、サーバ側で初期値を確定させる必要がある。
- **CTX-002**: `PUT` は部分更新ではなく全体置換として扱う必要がある。
- **CTX-003**: 一覧 API は再現可能な順序で返す必要がある。

## Decision

ToDo API は次の振る舞いで実装する。

- **DEC-001**: `POST /todos` は `completed=false`、`createdAt=updatedAt=now` をサーバ側で設定する。
- **DEC-002**: `PUT /todos/{todoId}` は全体置換とし、未指定の optional 項目は未設定または `null` として扱う。
- **DEC-003**: `GET /todos` の並び順は `createdAt desc` に固定する。
- **DEC-004**: `limit` は `1-100`、`offset` は `0以上`、`completed` は `true/false` のみを受け付ける。
- **DEC-005**: `total` はフィルタリング前の全件数を返す。

この決定により、作成・更新の結果が明確になり、一覧のテストが安定する。特に `createdAt desc` を固定することで、ページングや追加・削除の影響を受けにくくなる。

## Consequences

### Positive

- **POS-001**: 作成時の初期値が一貫し、クライアント側の期待値が明確になる。
- **POS-002**: 全体置換のルールが明確なため、更新ロジックの解釈がぶれにくい。
- **POS-003**: 一覧順序が固定されることで、テストとデバッグがしやすい。
- **POS-004**: ページングとフィルタの制約が明確になり、不正な入力を早く弾ける。
- **POS-005**: `total` の定義が固定されるため、UI 側で件数表示を実装しやすい。

### Negative

- **NEG-001**: `PUT` の全体置換は、部分更新に慣れた利用者には扱いづらい。
- **NEG-002**: `createdAt desc` 固定は、古い順に見たい利用ケースにはそのままでは合わない。
- **NEG-003**: `total` をフィルタ前件数にするため、ページ数の直感とずれる可能性がある。
- **NEG-004**: 厳格な入力制約により、クライアントの実装ミスが露見しやすい。

## Alternatives Considered

### `PUT` を部分更新にする

- **ALT-001**: **説明**: 未指定項目は既存値を保持し、差分のみを更新する。
- **ALT-002**: **不採用理由**: 仕様上は全体置換が前提であり、意味が曖昧になるため採用しない。

### 一覧順序を未定義にする

- **ALT-003**: **説明**: DB の返却順に任せる。
- **ALT-004**: **不採用理由**: テストが不安定になり、ページング結果も再現しにくくなる。

### `limit` と `offset` をより緩くする

- **ALT-005**: **説明**: 上限や下限を広げ、入力を寛容にする。
- **ALT-006**: **不採用理由**: 小規模 API では制約を明確にした方がバグを減らせる。

### `total` を現在ページ件数にする

- **ALT-007**: **説明**: `total` を返却件数に揃える。
- **ALT-008**: **不採用理由**: ページング UI に必要な総件数の意味を失う。

## Implementation Notes

- **IMP-001**: `POST` では、サーバ時刻を唯一の基準として初期値を設定する。
- **IMP-002**: `PUT` のバリデーションは、リクエストモデルとドメインモデルの役割を分けて実装する。
- **IMP-003**: 一覧 API は DB クエリで明示的にソートし、暗黙の順序に頼らない。
- **IMP-004**: ページング境界値はテストケースとして固定し、回帰を防ぐ。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0002: OpenAPI Contract as Source of Truth
- **REF-003**: ADR-0005: Date and Time Conventions
