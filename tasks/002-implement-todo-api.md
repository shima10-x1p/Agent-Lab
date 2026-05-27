# 002 Implement ToDo API

## 目的

Reference Draft に沿って ToDo の CRUD、完了/未完了切り替え、ページネーションを実装する。

## 参照するReference

- `docs/reference/todo-api.md`

## 参照するADR

- `docs/adr/0001-use-sqlite-for-initial-todo-storage.md`
- `docs/adr/0002-use-layered-fastapi-structure.md`
- `docs/adr/0003-use-sqlmodel-for-sqlite-access.md`

## 対象ファイル

想定:

- `app/api/`
- `app/schemas/`
- `app/db/`
- `app/repositories/`
- `app/services/`（必要な場合のみ）
- `tests/`

## やること

- `Todo`、`CreateTodoRequest`、`UpdateTodoRequest`、`SetTodoCompletionRequest` のスキーマを定義する。
- SQLModel で SQLite に ToDo を保存するテーブルまたはモデルを用意する。
- 次のエンドポイントを実装する。
  - `POST /todos`
  - `GET /todos?limit=&offset=`
  - `GET /todos/{todo_id}`
  - `PATCH /todos/{todo_id}`
  - `PATCH /todos/{todo_id}/completion`
  - `DELETE /todos/{todo_id}`
- `404 Not Found`、`400 Bad Request`、`422 Unprocessable Entity` の扱いを Reference に合わせる。
- テストでは本番用 DB ファイルを使わないようにする。

## やらないこと

- 認証・認可
- 検索・状態フィルタ
- ユーザー管理
- PostgreSQL 対応

## 完了条件

- Reference Draft の全エンドポイントが実装されている。
- バリデーションルールが Reference Draft と一致している。
- 存在しない ToDo に対して `404 Not Found` を返す。
- 削除成功時に `204 No Content` を返す。

## テスト条件

- 作成、一覧、取得、更新、完了切り替え、削除の正常系テストがある。
- バリデーションエラーのテストがある。
- 存在しない `todo_id` の `404` テストがある。
- ページネーションの `limit` / `offset` テストがある。

## 手作業確認項目

- OpenAPI UI で各エンドポイントを実行できる。
- アプリケーション再起動後も SQLite に保存した ToDo が残る。

## 未確定事項

- DB マイグレーションツールを導入するかは、初期実装では保留する。単一テーブルの初期作成で足りない変更が発生したら再判断する。