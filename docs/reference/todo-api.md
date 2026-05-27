# ToDo API Reference Draft

Status: Draft  
Date: 2026-05-28

## Scope

FastAPI を使用した ToDo 操作用マイクロサービスの HTTP API 仕様を定義する。

対象範囲:

- ToDo の作成、一覧取得、単体取得、更新、削除
- ToDo の完了/未完了切り替え
- 一覧取得のページネーション
- SQLite による永続化
- Docker による起動構成

対象外:

- 認証・認可
- ユーザーごとの ToDo 分離
- キーワード検索や状態フィルタ
- 外部サービス連携

## Base URL

ローカル開発では次を想定する。

```text
http://localhost:8000
```

## Authentication

認証は不要。

## Resource Schema

### Todo

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | integer | yes | ToDo の一意識別子 |
| `title` | string | yes | ToDo のタイトル |
| `description` | string or null | no | ToDo の詳細 |
| `completed` | boolean | yes | 完了状態 |
| `created_at` | string, date-time | yes | 作成日時 |
| `updated_at` | string, date-time | yes | 最終更新日時 |

### CreateTodoRequest

| Field | Type | Required | Validation |
|---|---|---:|---|
| `title` | string | yes | 1 文字以上、200 文字以下 |
| `description` | string or null | no | 1000 文字以下 |

### UpdateTodoRequest

すべてのフィールドは任意。少なくとも 1 フィールドは指定する。

| Field | Type | Required | Validation |
|---|---|---:|---|
| `title` | string | no | 1 文字以上、200 文字以下 |
| `description` | string or null | no | 1000 文字以下 |
| `completed` | boolean | no | なし |

### SetTodoCompletionRequest

| Field | Type | Required | Validation |
|---|---|---:|---|
| `completed` | boolean | yes | なし |

## Error Format

FastAPI / Pydantic の標準バリデーションエラー形式を基本とする。

アプリケーション固有エラーは次の形式を返す。

```json
{
  "detail": "Todo not found"
}
```

## Endpoints

### Health Check

```http
GET /health
```

#### Response

Status: `200 OK`

```json
{
  "status": "ok"
}
```

### Create Todo

```http
POST /todos
```

#### Request body

`CreateTodoRequest`

#### Response

Status: `201 Created`

Body: `Todo`

### List Todos

```http
GET /todos?limit=20&offset=0
```

#### Query parameters

| Parameter | Type | Required | Default | Validation |
|---|---|---:|---:|---|
| `limit` | integer | no | 20 | 1 以上、100 以下 |
| `offset` | integer | no | 0 | 0 以上 |

#### Response

Status: `200 OK`

```json
{
  "items": [
    {
      "id": 1,
      "title": "Write API reference",
      "description": "Draft the ToDo API contract",
      "completed": false,
      "created_at": "2026-05-28T10:00:00Z",
      "updated_at": "2026-05-28T10:00:00Z"
    }
  ],
  "limit": 20,
  "offset": 0,
  "total": 1
}
```

### Get Todo

```http
GET /todos/{todo_id}
```

#### Path parameters

| Parameter | Type | Required | Validation |
|---|---|---:|---|
| `todo_id` | integer | yes | 1 以上 |

#### Response

Status: `200 OK`  
Body: `Todo`

#### Errors

- `404 Not Found`: ToDo が存在しない

### Update Todo

```http
PATCH /todos/{todo_id}
```

#### Request body

`UpdateTodoRequest`

#### Response

Status: `200 OK`  
Body: `Todo`

#### Errors

- `400 Bad Request`: 更新フィールドが空
- `404 Not Found`: ToDo が存在しない
- `422 Unprocessable Entity`: バリデーションエラー

### Set Todo Completion

```http
PATCH /todos/{todo_id}/completion
```

#### Request body

`SetTodoCompletionRequest`

#### Response

Status: `200 OK`  
Body: `Todo`

#### Errors

- `404 Not Found`: ToDo が存在しない
- `422 Unprocessable Entity`: バリデーションエラー

### Delete Todo

```http
DELETE /todos/{todo_id}
```

#### Response

Status: `204 No Content`

#### Errors

- `404 Not Found`: ToDo が存在しない

## Status Codes

| Status | Usage |
|---:|---|
| 200 | 取得・更新成功 |
| 201 | 作成成功 |
| 204 | 削除成功 |
| 400 | リクエスト内容が仕様上不正 |
| 404 | 対象リソースが存在しない |
| 422 | Pydantic バリデーションエラー |
| 500 | 想定外のサーバーエラー |

## Persistence

- 初期実装では SQLite を使用する。
- SQLite アクセスには SQLModel を使用する。
- DB ファイルはローカル実行と Docker 実行の両方で扱える構成にする。
- テストでは本番用 DB ファイルを直接使用しない。

## Open Questions

- なし。初期計画に必要な保存方式、DBアクセス方式、API範囲、認証、配布形態はユーザー確認済み。