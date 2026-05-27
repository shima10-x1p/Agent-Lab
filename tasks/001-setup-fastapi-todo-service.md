# 001 Setup FastAPI ToDo Service

## 目的

FastAPI ToDo マイクロサービスの土台を作成し、ローカル実行できる状態にする。

## 参照するReference

- `docs/reference/todo-api.md`

## 参照するADR

- `docs/adr/0001-use-sqlite-for-initial-todo-storage.md`
- `docs/adr/0002-use-layered-fastapi-structure.md`
- `docs/adr/0003-use-sqlmodel-for-sqlite-access.md`

## 対象ファイル

想定:

- `pyproject.toml`
- `README.md`
- `app/main.py`
- `app/api/`
- `app/schemas/`
- `app/db/`
- `app/repositories/`

## やること

- FastAPI と ASGI サーバー依存関係を追加する。
- SQLModel を SQLite アクセス用ライブラリとして追加する。
- 軽量レイヤード構成のディレクトリを作成する。
- `GET /health` を実装する。
- アプリケーション起動コマンドを README に記載する。
- Python 3.14 設定と依存ライブラリの対応状況を確認する。

## やらないこと

- ToDo CRUD の全実装
- Docker 構成
- 認証・認可

## 完了条件

- FastAPI アプリケーションが起動する。
- `GET /health` が `200 OK` と `{ "status": "ok" }` を返す。
- 依存関係が `pyproject.toml` に反映されている。
- README にローカル起動方法がある。

## テスト条件

- ヘルスチェックの自動テストを追加する。
- プロジェクトで採用するテストコマンドを README に記載する。

## 手作業確認項目

- ローカルでアプリケーションを起動できる。
- ブラウザまたは HTTP クライアントで `/health` を確認できる。

## 未確定事項

- なし。DBアクセス方式は SQLModel でユーザー確認済み。