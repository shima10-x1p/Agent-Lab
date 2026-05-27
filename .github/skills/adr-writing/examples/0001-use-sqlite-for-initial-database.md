# ADR-0001: Use SQLite for Initial Database

## Status

Proposed

## Date

2026-05-27

## Context

ToDo APIの初期実装では、小規模・学習用・ローカル開発を優先する。

現時点では、複数ユーザーによる同時利用や本番運用を主目的にしていない。まずはAPI、データモデル、永続化、テストの流れをシンプルに確認できることが重要である。

DB選定を曖昧にしたまま実装を進めると、Repository層、テスト方法、開発環境、データ初期化手順が揺れやすくなる。Reference Draftや作業手順書でも、永続化方式を前提にした記述が必要になる。

## Decision Drivers

- Simplicity
- Local development experience
- Testability
- Operational cost
- Learning cost
- Compatibility with small ToDo API scope
- Future extensibility

## Considered Options

### Option 1: SQLite

Pros:

- ローカル環境で追加のDBサーバーを起動せずに利用できる。
- 小規模なToDo APIでは十分な機能を持つ。
- ファイルベースで扱えるため、学習用・検証用のセットアップが簡単になる。
- テスト時に一時DBを作りやすい。
- 初期の運用コストが低い。

Cons:

- 高い同時書き込み性能は期待しにくい。
- 本番運用や複数ユーザー対応では、PostgreSQLなどへの移行が必要になる可能性がある。
- DB固有機能を使い始めると、将来の移行コストが発生する。

### Option 2: PostgreSQL

Pros:

- 本番運用や複数ユーザー利用に向いている。
- トランザクション、制約、インデックス、拡張機能が充実している。
- 将来的なスケールを見据えやすい。

Cons:

- 初期セットアップにDBサーバーや接続設定が必要になる。
- 学習用・ローカル開発では運用コストが相対的に高い。
- 小規模な初期実装では複雑さが先行しやすい。

### Option 3: In-memory DB

Pros:

- セットアップが最も簡単である。
- テストやプロトタイプでは高速に扱える。
- 永続化を考えずにAPIの形だけを確認しやすい。

Cons:

- アプリケーション再起動でデータが失われる。
- 永続化を前提にしたRepository設計やマイグレーション検討が後回しになる。
- 実際のDB利用時に設計変更が発生しやすい。

## Decision

ToDo APIの初期DBとしてSQLiteを採用する。

初期実装では、ローカル開発と学習容易性を優先し、追加のDBサーバーを必要としない構成にする。Repository層では将来のDB移行を妨げないように、DBアクセスの詳細をアプリケーションロジックから分離する。

## Consequences

Positive:

- ローカル開発の開始が簡単になる。
- 学習用・小規模APIとして、永続化の流れを理解しやすい。
- テスト用DBを作成しやすくなる。
- 初期の運用コストを抑えられる。

Negative:

- 複数ユーザーや高い同時書き込みが必要になった場合、SQLiteでは不足する可能性がある。
- 本番運用を始める前に、PostgreSQLなどへの移行検討が必要になる可能性がある。

Neutral / Trade-offs:

- 初期速度と簡単さを優先し、将来のスケール対応は見直し条件として扱う。
- DB移行の可能性に備えるため、Repository層でDB依存を局所化する必要がある。

## Confidence

Medium

現時点の小規模・学習用・ローカル開発という前提では妥当性が高い。一方で、本番運用や複数ユーザー対応の要件が明確になると、PostgreSQLへの変更が必要になる可能性がある。

## Revisit When

- 複数ユーザー対応が必要になったとき
- 本番運用が必要になったとき
- 同時書き込み性能が問題になったとき
- DBマイグレーションやバックアップ運用が必要になったとき
- ToDo以外の複雑なデータモデルを扱うようになったとき

## Related Documents

- docs/reference/todo-api.md
- docs/adr/0002-use-layered-architecture.md
- tasks/implement-todo-api.md
