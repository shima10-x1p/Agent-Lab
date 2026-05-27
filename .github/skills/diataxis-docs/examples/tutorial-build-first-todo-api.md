# Tutorial: Build your first ToDo API with FastAPI

## What you will build

FastAPIを使って、最小構成のToDo APIを作る。

このTutorialでは、次の操作ができるAPIを完成させる。

- ToDo一覧を取得する
- ToDoを作成する
- ToDoを更新する
- ToDoを削除する

詳細なAPI仕様は`docs/reference/todo-api.md`を参照する。

## What you will learn

- FastAPIアプリの基本構成
- ルーティングの作り方
- リクエスト/レスポンススキーマの考え方
- APIを起動して動作確認する流れ

## Prerequisites

- Pythonの基本的な実行方法を知っている
- HTTPのGET / POST / PATCH / DELETEの意味を大まかに知っている
- 作業用ディレクトリを用意している

## Starting point

空のPythonプロジェクトから始める。

最初はデータベースを使わず、メモリ上のリストでToDoを管理する。永続化方式は学習の主目的ではないため、このTutorialでは深追いしない。

## Steps

1. FastAPIアプリを作成する
   - アプリケーションの入口を用意する
   - ヘルスチェック用のエンドポイントを作る

2. ToDoの形を決める
   - 作成用スキーマを用意する
   - 読み取り用スキーマを用意する
   - 更新用スキーマを用意する

3. ToDo一覧を返す
   - `GET /todos`で現在のToDo一覧を返す
   - 最初は空の配列が返ればよい

4. ToDoを作成する
   - `POST /todos`でタイトルを受け取る
   - 作成したToDoにIDを付ける
   - 作成結果をレスポンスとして返す

5. ToDoを更新する
   - `PATCH /todos/{id}`で指定したToDoを更新する
   - 見つからないIDの場合はエラーを返す

6. ToDoを削除する
   - `DELETE /todos/{id}`で指定したToDoを削除する
   - 削除できたら空のレスポンスを返す

7. APIドキュメントで確認する
   - FastAPIの自動生成ドキュメントを開く
   - 各エンドポイントを順番に試す

## Check your work

次の操作ができれば成功。

- ToDoを1件作成できる
- 作成したToDoが一覧に表示される
- ToDoのタイトルや完了状態を更新できる
- ToDoを削除できる
- 存在しないIDを指定したときにエラーになる

## What happened

このTutorialでは、FastAPIのルーティングとスキーマを使って、最小限のToDo APIを作った。

学習のため、永続化、認証、ページング、詳細なエラー形式は最小限にしている。実務で必要な仕様はReferenceやHow-toで確認する。

## Next steps

* docs/how-to/add-due-date-to-todo.md
* docs/reference/todo-api.md
* docs/explanation/todo-architecture-overview.md
