# ToDo Architecture Overview Explanation

## Summary

ToDo APIは、HTTPリクエストを受け取るrouter、入出力の形を定義するschema、永続化対象を表すmodel、データアクセスを担当するrepository、業務ルールを扱うserviceに分けて構成する。

この分割により、API仕様、業務ルール、データ保存の責務を分けて理解しやすくする。

## Background

ToDo APIは小さなアプリケーションでも、機能追加が進むと次のような関心が混ざりやすい。

- HTTPの詳細
- 入力検証
- 業務ルール
- データ保存
- レスポンス形式
- テスト対象

すべてを1つのファイルや関数に集めると、変更の影響範囲が分かりにくくなる。

## Problem

たとえば`due_date`や認証を追加するとき、routerにすべての処理が集まっていると、API仕様の変更なのか、業務ルールの変更なのか、保存形式の変更なのかが判別しにくい。

その結果、テストしにくくなり、Reference Draftと実装の対応も追いにくくなる。

## Concepts

### router

routerはHTTPリクエストとレスポンスの境界を扱う。

主な責務:

- URLパスとHTTPメソッドを定義する
- リクエストを受け取る
- serviceを呼び出す
- HTTPステータスコードを返す

### schema

schemaはAPIの入出力の形を定義する。

主な責務:

- Request bodyの構造を表す
- Response bodyの構造を表す
- 入力値の基本的な検証を行う
- Reference Draftのスキーマと対応する

### model

modelは永続化対象のデータ構造を表す。

主な責務:

- データベースに保存する項目を定義する
- ID、作成日時、更新日時など保存上必要な情報を持つ

### repository

repositoryはデータアクセスを担当する。

主な責務:

- ToDoを保存する
- ToDoを取得する
- ToDoを更新する
- ToDoを削除する
- DBやストレージの詳細をserviceから隠す

### service

serviceは業務ルールを扱う。

主な責務:

- ToDo作成や更新のユースケースを表す
- 複数repositoryをまたぐ処理をまとめる
- 業務上の検証を行う
- routerからデータ保存の詳細を分離する

## Design overview

典型的な処理の流れは次の通り。

1. routerがHTTPリクエストを受け取る
2. schemaが入力の形を検証する
3. routerがserviceを呼び出す
4. serviceが業務ルールを適用する
5. serviceがrepositoryを使ってデータを読み書きする
6. repositoryがmodelを永続化する
7. serviceが結果を返す
8. routerがschemaに合わせてレスポンスを返す

この構成では、ReferenceはAPI境界であるrouter/schemaと強く関係する。ADRは、レイヤー構造やDB選定などの後戻りしにくい判断を記録する。

## Trade-offs

### Benefits

- 変更の影響範囲を追いやすい
- API仕様と内部実装を分けやすい
- serviceやrepositoryを単体でテストしやすい
- 将来DBや認証方式を変えるときに境界を保ちやすい

### Costs

- 小さな機能でもファイル数が増える
- 初学者には責務の分割が少し難しく見える
- 単純なCRUDだけなら過剰に感じる場合がある

## Related ADRs

* docs/adr/0001-use-sqlite-for-initial-database.md
* docs/adr/0002-use-layered-architecture.md

## Related Reference

* docs/reference/todo-api.md

## Further reading

* docs/how-to/add-due-date-to-todo.md
* docs/tutorials/build-first-todo-api.md
