# 0001 Use SQLite for Initial ToDo Storage

Status: Proposed  
Date: 2026-05-28

## Context

FastAPI を使用して ToDo 操作用マイクロサービスを作成する。初期段階では認証なし、単一サービス、CRUD と完了/未完了切り替え、ページネーションを提供する。

ToDo データはプロセス再起動後も保持する必要があるため、インメモリ保存だけでは不十分である。一方で、初期実装では PostgreSQL のような外部 DB サーバーを必須にすると開発・検証のセットアップが重くなる。

## Decision Drivers

- ローカル開発と Docker 実行の手軽さ
- 初期実装のシンプルさ
- データ永続化の必要性
- 後から PostgreSQL などへ移行できる余地
- テスト容易性

## Considered Options

### SQLite

Pros:

- 追加の DB サーバーなしで永続化できる
- ローカル開発と CI で扱いやすい
- 小規模 ToDo サービスの初期実装に十分
- テスト用 DB を分離しやすい

Cons:

- 高い同時書き込み負荷には向かない
- 複数インスタンス運用では DB ファイル共有が課題になる

### In-memory storage

Pros:

- 実装が最も単純
- 外部依存がない

Cons:

- プロセス再起動でデータが消える
- マイクロサービスとしての実用性が低い

### PostgreSQL

Pros:

- 本番運用に向きやすい
- 複数インスタンスや同時アクセスに強い

Cons:

- 初期セットアップが重い
- Docker Compose や接続設定の複雑さが増える

## Decision

初期実装では SQLite を採用する。

永続化層は、将来 PostgreSQL へ移行しやすいように API 層へ直接依存させず、データアクセス責務を分離する。

## Consequences

### Positive

- 小さく動く ToDo マイクロサービスを素早く構築できる
- ローカル実行、Docker 実行、テストで DB を分離しやすい
- 外部 DB サーバーなしで永続化を実現できる

### Negative

- 本格的な水平スケールや高負荷書き込みには適さない
- PostgreSQL 移行時には接続設定、マイグレーション、SQL 方言差分の確認が必要になる

### Neutral or Trade-offs

- 初期実装では運用の単純さを優先し、本番相当の DB 構成は後続判断に回す

## Confidence

High

ユーザー確認で SQLite が選択され、初期サービスの規模にも合っているため。

## Revisit When

- 複数アプリケーションインスタンスで運用する
- 同時書き込みが増える
- 本番環境で PostgreSQL などの外部 DB が必要になる
- ユーザーごとのデータ分離や認証を追加する

## Related Documents

- [ToDo API Reference Draft](../reference/todo-api.md)
- [Task 001](../../tasks/001-setup-fastapi-todo-service.md)
- [Task 002](../../tasks/002-implement-todo-api.md)