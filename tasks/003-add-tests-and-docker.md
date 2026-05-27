# 003 Add Tests and Docker Runtime

## 目的

ToDo マイクロサービスを自動テストで検証し、Docker で起動できる状態にする。

## 参照するReference

- `docs/reference/todo-api.md`

## 参照するADR

- `docs/adr/0001-use-sqlite-for-initial-todo-storage.md`
- `docs/adr/0002-use-layered-fastapi-structure.md`
- `docs/adr/0003-use-sqlmodel-for-sqlite-access.md`

## 対象ファイル

想定:

- `tests/`
- `Dockerfile`
- `.dockerignore`
- `README.md`
- 必要に応じて `docker-compose.yml`

## やること

- API テストを `tests/` 配下に整理する。
- ローカル実行用と Docker 実行用の手順を README に記載する。
- Dockerfile を作成する。
- SQLite DB ファイルや仮想環境などを Docker build context から除外する。
- Docker 実行時に SQLite DB の保存先を明確にする。

## やらないこと

- PostgreSQL コンテナの追加
- 認証・認可
- CI 設定
- 本番向けオーケストレーション設定

## 完了条件

- テストがすべて通る。
- Docker イメージをビルドできる。
- Docker コンテナで API が起動する。
- コンテナ上の `/health` が `200 OK` を返す。
- README にテスト、ローカル起動、Docker 起動の手順がある。

## テスト条件

- HTTP API の正常系・異常系テストを実行する。
- テスト DB と通常実行 DB が分離されていることを確認する。

## 手作業確認項目

- Docker コンテナ起動後に `/docs` を開ける。
- Docker コンテナ起動後に ToDo 作成・一覧取得ができる。

## 未確定事項

- `docker-compose.yml` を作るか、単体 `Dockerfile` のみにするかは実装時の永続化方式に合わせて判断する。