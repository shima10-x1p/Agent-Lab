# ADR-0002: Use Layered Architecture

## Status

Proposed

## Date

2026-05-27

## Context

FastAPIでToDo APIを実装するにあたり、`main.py` にすべての処理を書く単一構成にするか、責務ごとにファイルやモジュールを分けるかを決める必要がある。

ToDo APIは初期段階では小規模だが、今後はデータモデル、バリデーション、DBアクセス、ビジネスルール、テストが増える可能性がある。また、Copilotに実装を依頼する場合、作業単位が小さく責務が明確な構成のほうが、変更範囲を限定しやすい。

構成を決めないまま実装を進めると、APIルーティング、スキーマ、DBモデル、永続化処理、サービスロジックが混在し、保守やテストが難しくなるリスクがある。

## Decision Drivers

- Maintainability
- Testability
- Simplicity
- Separation of concerns
- Future extensibility
- Compatibility with Copilot-assisted implementation
- Compatibility with existing design

## Considered Options

### Option 1: Layered architecture with router / schema / model / repository / service

Pros:

- ルーティング、入出力スキーマ、DBモデル、永続化、ビジネスロジックの責務を分離できる。
- テスト対象を層ごとに分けやすい。
- DB変更やビジネスルール追加時の影響範囲を把握しやすい。
- Copilotに「repositoryを実装する」「serviceをテストする」のような小さな作業単位で依頼しやすい。
- Reference Draftや作業手順書で、実装対象を明確に書きやすい。

Cons:

- 初期ファイル数が増える。
- 非常に小さいアプリでは、分割の負担が実装量に対して大きく感じられる可能性がある。
- 層の責務が曖昧なままだと、かえって冗長な構成になる。

### Option 2: Single `main.py` structure

Pros:

- 初期実装が最も簡単である。
- 小さなサンプルでは全体像を1ファイルで把握できる。
- ディレクトリ構成を考える時間を減らせる。

Cons:

- API、スキーマ、DBアクセス、ビジネスロジックが混在しやすい。
- テスト対象を分離しにくい。
- 機能追加時に `main.py` が肥大化しやすい。
- Copilotに依頼する作業範囲が大きくなり、意図しない変更が入りやすい。

## Decision

FastAPIアプリは、`router` / `schema` / `model` / `repository` / `service` に分けるレイヤー構造を採用する。

各層の責務は次のように扱う。

- `router`: HTTPエンドポイントとリクエスト/レスポンスの受け渡し
- `schema`: API入出力の型とバリデーション
- `model`: DB永続化に使うデータモデル
- `repository`: DBアクセスの詳細
- `service`: ユースケースやビジネスルール

## Consequences

Positive:

- 責務が分離され、保守しやすくなる。
- テストを層ごとに設計しやすくなる。
- DB変更やビジネスルール追加の影響範囲を限定しやすい。
- Copilotに小さな作業単位で実装やレビューを依頼しやすくなる。
- Reference Draftやtasksで作業対象を明確に示しやすい。

Negative:

- 初期段階ではファイル数が増え、単一ファイル構成よりも見通しが悪く感じられる可能性がある。
- 小さすぎるアプリでは、レイヤー分割が過剰設計になる可能性がある。

Neutral / Trade-offs:

- 初期の簡潔さよりも、責務分離と今後の変更容易性を優先する。
- 分割の負担を抑えるため、各層には必要な責務だけを置き、抽象化を増やしすぎない。

## Confidence

Medium

ToDo APIが学習用かつ小規模である点を考えると、単一 `main.py` でも成立する。一方で、Copilotに小さな作業単位で実装させやすくする目的と、将来の保守性を考えると、レイヤー構造を採用する価値がある。

## Revisit When

- アプリが小さすぎて、分割の負担が明らかに大きいと判断したとき
- レイヤー間の責務が曖昧になり、実装が冗長になったとき
- 機能が増えず、単一ファイル構成のほうが保守しやすいと分かったとき
- ドメインロジックが複雑化し、より明確なアーキテクチャ境界が必要になったとき

## Related Documents

- docs/reference/todo-api.md
- docs/adr/0001-use-sqlite-for-initial-database.md
- tasks/implement-todo-api.md
