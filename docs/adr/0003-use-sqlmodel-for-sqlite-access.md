# 0003 Use SQLModel for SQLite Access

Status: Proposed  
Date: 2026-05-28

## Context

ToDo マイクロサービスでは、SQLite を初期永続化方式として採用する。FastAPI でリクエスト/レスポンススキーマを扱いつつ、SQLite テーブルへの読み書きも実装する必要がある。

標準 `sqlite3` は依存を増やさずに使えるが、モデル定義、バリデーション、型、テスト用 DB の差し替えを手作業で管理しやすい。SQLAlchemy は柔軟で広く使われるが、初期 ToDo API には記述量が増えやすい。

## Decision Drivers

- FastAPI / Pydantic との相性
- 初期実装の読みやすさ
- SQLite での実装容易性
- 将来の DB 移行余地
- テスト容易性

## Considered Options

### SQLModel

Pros:

- FastAPI と Pydantic の利用体験に近い
- 小規模 CRUD API でモデル定義を簡潔に保ちやすい
- SQLAlchemy を土台にしており、将来の拡張余地がある
- ユーザーが選択済み

Cons:

- SQLAlchemy より抽象度が高く、細かな制御では制約になる可能性がある
- プロジェクト依存関係が増える

### SQLAlchemy

Pros:

- Python の標準的な ORM として実績がある
- 複雑なクエリや高度な設定に対応しやすい

Cons:

- 初期 ToDo API にはやや記述量が多い
- Pydantic スキーマとの対応を別途管理する必要がある

### Standard sqlite3

Pros:

- 追加依存が不要
- SQLite の挙動を直接扱える

Cons:

- SQL と型変換を手作業で管理する必要がある
- スキーマ、バリデーション、レスポンスモデルとの重複が増えやすい

## Decision

SQLite アクセスには SQLModel を採用する。

## Consequences

### Positive

- FastAPI のスキーマ定義と DB モデルを近い形で扱える
- 小規模 CRUD の実装量を抑えられる
- テスト用 SQLite DB を差し替えやすい

### Negative

- SQLModel への依存が追加される
- 高度な ORM 制御が必要になった場合、SQLAlchemy の知識が必要になる

### Neutral or Trade-offs

- SQLModel は SQLAlchemy を土台にしているため、単純さと拡張余地の中間案として扱う

## Confidence

High

ユーザー確認で SQLModel が選択され、FastAPI と SQLite の初期 CRUD 実装に合っているため。

## Revisit When

- 複雑なクエリやトランザクション制御が増える
- PostgreSQL などへ移行する
- SQLModel の対応 Python バージョンや依存関係で問題が出る

## Related Documents

- [ToDo API Reference Draft](../reference/todo-api.md)
- [ADR 0001](0001-use-sqlite-for-initial-todo-storage.md)
- [Task 001](../../tasks/001-setup-fastapi-todo-service.md)
- [Task 002](../../tasks/002-implement-todo-api.md)