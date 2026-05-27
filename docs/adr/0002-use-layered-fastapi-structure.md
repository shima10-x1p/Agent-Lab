# 0002 Use Layered FastAPI Structure

Status: Proposed  
Date: 2026-05-28

## Context

ToDo マイクロサービスは初期実装としては小規模だが、API 仕様、バリデーション、永続化、テスト、Docker 起動を含む。API ハンドラーに永続化処理を直接書くと、機能追加や DB 変更時に変更範囲が広がりやすい。

一方で、過度に複雑なクリーンアーキテクチャを導入すると、初期サービスとしてはファイル数や抽象化が増えすぎる。

## Decision Drivers

- FastAPI らしいシンプルな構成
- API 層と永続化層の分離
- テスト容易性
- 将来の DB 移行や機能追加のしやすさ
- 過度な抽象化を避けること

## Considered Options

### Minimal single-file app

Pros:

- 最も早く実装できる
- 学習用には分かりやすい

Cons:

- API、スキーマ、永続化が混在しやすい
- テストや将来変更で影響範囲が広がる

### Lightweight layered structure

Pros:

- API、スキーマ、永続化、設定を分けられる
- 小規模でも見通しがよい
- テスト時に DB や依存関係を差し替えやすい

Cons:

- 単一ファイルより初期ファイル数が増える
- 層の責務を守る必要がある

### Full clean architecture

Pros:

- 大規模化に強い
- ビジネスルールと外部技術の分離が明確

Cons:

- 今回の初期 ToDo サービスには重い
- 抽象化が増え、実装速度と読みやすさが落ちる可能性がある

## Decision

軽量なレイヤード構成を採用する。

想定する主な責務分離:

- `app/main.py`: FastAPI アプリケーション生成、ルーター登録
- `app/api/`: HTTP エンドポイント
- `app/schemas/`: リクエスト/レスポンススキーマ
- `app/models/` または `app/db/`: DB モデルと接続管理
- `app/repositories/`: ToDo 永続化操作
- `app/services/`: 必要な場合のみユースケース処理
- `tests/`: テストコード

## Consequences

### Positive

- API と永続化の責務が分かれ、テストしやすい
- 将来 PostgreSQL や認証を追加する場合の変更範囲を抑えやすい
- `src` 配下にテストを混ぜない構成にできる

### Negative

- 初期実装としては単一ファイルより構成が増える
- 小さな機能でもファイル間の対応を理解する必要がある

### Neutral or Trade-offs

- `services/` は必要になった時点で使い、単純な CRUD を過剰に抽象化しない

## Confidence

Medium

初期 ToDo API には妥当だが、実装時に使用する ORM / DB アクセス方式によって最適な分割が少し変わるため。

## Revisit When

- 認証やユーザー管理を追加する
- 外部サービス連携を追加する
- ドメインロジックが CRUD を大きく超える
- DB 技術を変更する

## Related Documents

- [ToDo API Reference Draft](../reference/todo-api.md)
- [Task 001](../../tasks/001-setup-fastapi-todo-service.md)
- [Task 002](../../tasks/002-implement-todo-api.md)