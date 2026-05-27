# ToDo API Reference Draft

## Overview

このReference Draftは、ToDo APIのエンドポイント、リクエスト/レスポンススキーマ、ステータスコード、エラー形式、バリデーションルールを定義する。

実装前はAPI契約の下書きとして扱い、実装後に実際の挙動と照合して更新する。

## Endpoints

### GET /todos

#### Description

ToDo一覧を取得する。

#### Request

##### Path Parameters

| Name | Type | Required | Description |
|---|---|---:|---|

##### Query Parameters

| Name | Type | Required | Description |
|---|---|---:|---|
| limit | integer | No | 取得件数。デフォルトは20。 |
| offset | integer | No | 取得開始位置。デフォルトは0。 |
| completed | boolean | No | 完了状態で絞り込む。 |
| sort | string | No | 並び順。例: `created_at`, `-created_at`, `due_date`。 |

##### Request Body

なし。

#### Response

##### Success

Status: 200

```json
{
  "items": [
    {
      "id": 1,
      "title": "Write API reference",
      "description": "Draft the ToDo API contract",
      "completed": false,
      "due_date": "2026-06-01",
      "created_at": "2026-05-27T10:00:00Z",
      "updated_at": "2026-05-27T10:00:00Z"
    }
  ],
  "limit": 20,
  "offset": 0,
  "total": 1
}
```

##### Errors

| Status | Code | Description |
| -----: | ---- | ----------- |
| 400 | invalid_query_parameter | Query parameterが不正。 |

### POST /todos

#### Description

新しいToDoを作成する。

#### Request

##### Path Parameters

| Name | Type | Required | Description |
|---|---|---:|---|

##### Query Parameters

| Name | Type | Required | Description |
|---|---|---:|---|

##### Request Body

```json
{
  "title": "Write API reference",
  "description": "Draft the ToDo API contract",
  "due_date": "2026-06-01"
}
```

#### Response

##### Success

Status: 201

```json
{
  "id": 1,
  "title": "Write API reference",
  "description": "Draft the ToDo API contract",
  "completed": false,
  "due_date": "2026-06-01",
  "created_at": "2026-05-27T10:00:00Z",
  "updated_at": "2026-05-27T10:00:00Z"
}
```

##### Errors

| Status | Code | Description |
| -----: | ---- | ----------- |
| 422 | validation_error | Request bodyの検証に失敗。 |

### PATCH /todos/{id}

#### Description

指定したToDoを部分更新する。

#### Request

##### Path Parameters

| Name | Type | Required | Description |
|---|---|---:|---|
| id | integer | Yes | 更新対象のToDo ID。 |

##### Query Parameters

| Name | Type | Required | Description |
|---|---|---:|---|

##### Request Body

```json
{
  "title": "Update API reference",
  "description": "Reflect implementation details",
  "completed": true,
  "due_date": "2026-06-05"
}
```

すべてのフィールドは任意。指定されたフィールドのみ更新する。

#### Response

##### Success

Status: 200

```json
{
  "id": 1,
  "title": "Update API reference",
  "description": "Reflect implementation details",
  "completed": true,
  "due_date": "2026-06-05",
  "created_at": "2026-05-27T10:00:00Z",
  "updated_at": "2026-05-27T11:00:00Z"
}
```

##### Errors

| Status | Code | Description |
| -----: | ---- | ----------- |
| 404 | todo_not_found | 指定したToDoが存在しない。 |
| 422 | validation_error | Request bodyの検証に失敗。 |

### DELETE /todos/{id}

#### Description

指定したToDoを削除する。

#### Request

##### Path Parameters

| Name | Type | Required | Description |
|---|---|---:|---|
| id | integer | Yes | 削除対象のToDo ID。 |

##### Query Parameters

| Name | Type | Required | Description |
|---|---|---:|---|

##### Request Body

なし。

#### Response

##### Success

Status: 204

レスポンスボディなし。

##### Errors

| Status | Code | Description |
| -----: | ---- | ----------- |
| 404 | todo_not_found | 指定したToDoが存在しない。 |

## Schemas

### TodoCreate

| Field | Type | Required | Description |
| ----- | ---- | -------: | ----------- |
| title | string | Yes | ToDoのタイトル。1〜120文字。 |
| description | string or null | No | ToDoの補足説明。最大1000文字。 |
| due_date | string or null | No | 締切日。ISO 8601の日付形式（`YYYY-MM-DD`）。 |

### TodoRead

| Field | Type | Required | Description |
| ----- | ---- | -------: | ----------- |
| id | integer | Yes | ToDo ID。 |
| title | string | Yes | ToDoのタイトル。 |
| description | string or null | No | ToDoの補足説明。 |
| completed | boolean | Yes | 完了状態。 |
| due_date | string or null | No | 締切日。ISO 8601の日付形式（`YYYY-MM-DD`）。 |
| created_at | string | Yes | 作成日時。ISO 8601の日時形式。 |
| updated_at | string | Yes | 更新日時。ISO 8601の日時形式。 |

### TodoUpdate

| Field | Type | Required | Description |
| ----- | ---- | -------: | ----------- |
| title | string | No | ToDoのタイトル。1〜120文字。 |
| description | string or null | No | ToDoの補足説明。最大1000文字。 |
| completed | boolean | No | 完了状態。 |
| due_date | string or null | No | 締切日。ISO 8601の日付形式（`YYYY-MM-DD`）。 |

### ErrorResponse

| Field | Type | Required | Description |
| ----- | ---- | -------: | ----------- |
| error.code | string | Yes | 機械判定用のエラーコード。 |
| error.message | string | Yes | 人間向けの短い説明。 |
| error.details | array | No | フィールド単位の詳細。 |

Example:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "title",
        "message": "title is required"
      }
    ]
  }
}
```

## Validation Rules

- `title`は必須。空文字不可。1〜120文字。
- `description`は任意。指定する場合は最大1000文字。
- `completed`はboolean。
- `due_date`は任意。指定する場合は`YYYY-MM-DD`形式。
- `limit`は1〜100。
- `offset`は0以上。

## Authentication

初期版では認証なし。

認証方式を追加する場合は、API仕様更新に加えてADR候補として扱う。

## Pagination

`GET /todos`は`limit`と`offset`によるページングを提供する。

## Sorting

`GET /todos`は`sort`で並び順を指定できる。

- `created_at`: 作成日時の昇順
- `-created_at`: 作成日時の降順
- `due_date`: 締切日の昇順

## Filtering

`GET /todos`は`completed`で完了状態を絞り込める。

## Notes

- この文書はReference Draftであり、設計理由は含めない。
- DB選定、レイヤー構造、認証方式はADR候補として扱う。

## Related Documents

* docs/how-to/add-due-date-to-todo.md
* docs/explanation/todo-architecture-overview.md
* docs/adr/0001-use-sqlite-for-initial-database.md
* tasks/001-create-todo-api.md
