# Agent Lab

OpenAPI 契約 (`docs/spec/openapi.yaml`) を正とする、FastAPI + ヘキサゴナルアーキテクチャの ToDo API マイクロサービスです。

## セットアップ

1. 依存同期: `uv sync --extra dev`
2. アプリ起動: `uv run python main.py`
3. テスト実行: `uv run pytest`

## 主な構成

- `src/agent_lab/domain/` — ドメインモデルとドメインエラー
- `src/agent_lab/application/` — ユースケースとポート
- `src/agent_lab/presentation/fastapi/` — FastAPI ルーター、依存解決、エラーハンドラー
- `src/agent_lab/infrastructure/` — SQLAlchemy / SQLite 実装、Clock
- `src/agent_lab/bootstrap/` — 設定、DI、OpenAPI、アプリ生成
- `src/agent_lab/generated/` — OpenAPI 由来 DTO
- `alembic/` — マイグレーション

## 契約と挙動

- 仕様書: `docs/spec/openapi.yaml`
- 一覧順序: `createdAt desc`
- `POST /todos` は `completed=false` で作成
- Validation error は `400` に正規化
- `GET /healthz` は運用確認用で OpenAPI 契約には含めません

## DB / 設定

環境変数は `.env` から読み込みます。デフォルトでは SQLite を利用します。

- `TODO_API_DATABASE_URL`
- `TODO_API_AUTO_CREATE_SCHEMA`

初期スキャフォールディングでは、ローカル実行とテストを簡単にするために起動時スキーマ作成を有効化しています。Alembic による初期マイグレーションも同梱しています。
