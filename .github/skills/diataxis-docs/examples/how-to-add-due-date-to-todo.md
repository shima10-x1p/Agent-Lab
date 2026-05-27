# How to add a due date to ToDo

## Goal

既存のToDo APIに`due_date`を追加し、作成・更新・取得時に締切日を扱えるようにする。

## When to use this guide

- 既存のToDo APIに締切日を追加したいとき
- API契約、データモデル、テスト、ドキュメントを一貫して更新したいとき
- 実装担当者へ作業の流れと確認観点を渡したいとき

## Prerequisites

- ToDo APIの基本機能が実装済みである
- `docs/reference/todo-api.md`が存在する
- 永続化方式とレイヤー構造に関するADRが存在する、またはADR候補として整理されている
- 既存のテスト実行方法が分かっている

## Steps

1. Referenceを更新する
   - `TodoCreate`、`TodoRead`、`TodoUpdate`に`due_date`を追加する
   - `POST /todos`、`PATCH /todos/{id}`、`GET /todos`の例を更新する
   - `due_date`の形式を`YYYY-MM-DD`としてValidation Rulesに記載する

2. 影響範囲を確認する
   - 入力スキーマ
   - レスポンススキーマ
   - 永続化モデル
   - Repositoryまたはデータアクセス層
   - Service層の検証ルール
   - APIテスト
   - 既存データの扱い

3. 必要なADR候補を確認する
   - 日付型を文字列として扱うか、日付型として扱うか
   - タイムゾーンを扱うか
   - 既存データのデフォルト値をどう扱うか

4. 実装タスクに分解する
   - スキーマ更新
   - モデル更新
   - 保存処理更新
   - APIレスポンス更新
   - テスト更新
   - Reference更新結果との照合

5. 動作確認する
   - `due_date`ありでToDoを作成できること
   - `due_date`なしでToDoを作成できること
   - `due_date`を更新できること
   - 不正な日付形式がValidation Errorになること
   - 一覧取得で`due_date`が返ること

## Verify the result

- `POST /todos`のレスポンスに`due_date`が含まれる
- `PATCH /todos/{id}`で`due_date`を変更できる
- `GET /todos`で各ToDoの`due_date`を確認できる
- `docs/reference/todo-api.md`のスキーマと実装結果が一致している
- 既存テストと追加テストが成功する

## Troubleshooting

- `due_date`がレスポンスに出ない場合は、読み取り用スキーマとレスポンス変換を確認する
- 不正な日付が保存される場合は、入力スキーマとService層の検証境界を確認する
- 既存データでエラーになる場合は、`due_date`を任意項目として扱えているか確認する
- 日付型やタイムゾーンの扱いで判断が必要な場合は、ADR候補として切り出す

## Related Reference

* docs/reference/todo-api.md

## Related ADRs

* docs/adr/0001-use-sqlite-for-initial-database.md
* docs/adr/0002-use-layered-architecture.md
* docs/adr/0003-store-due-date-as-date.md
