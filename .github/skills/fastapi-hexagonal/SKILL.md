---
name: fastapi-hexagonal
description: "Python+FastAPI ヘキサゴナルアーキテクチャ実装ガイド。Use when: FastAPI サービス作成, ルーター追加, ユースケース実装, リポジトリ実装, ドメインモデル作成, 新規プロジェクトのスキャフォールディング, ヘキサゴナルアーキテクチャ, DDD, クリーンアーキテクチャ, 依存性注入, OpenAPI コード生成, DI container."
argument-hint: "実装したい機能または操作内容（例: 'ユーザー作成API', 'スキャフォールディング'）"
---

# FastAPI Hexagonal Architecture

Python + FastAPI を使ったヘキサゴナルアーキテクチャの実装ガイド。
中心に `domain` / `application` を置き、外側に `presentation` / `infrastructure` を配置する。

## 参照ファイル

- [レイヤー詳細](./references/layers.md) — 各レイヤーの役割・置くもの・禁止事項
- [スキャフォールディング](./references/scaffolding.md) — 新規プロジェクトのディレクトリ生成手順

## ディレクトリ構成

```
src/
└─ <package_name>/
   ├─ __init__.py
   ├─ main.py
   ├─ generated/
   │  ├─ README.md
   │  ├─ apis/
   │  └─ models/
   ├─ presentation/
   │  └─ fastapi/
   │     ├─ routers/
   │     ├─ dependencies.py
   │     └─ error_handlers.py
   ├─ application/
   │  ├─ use_cases/
   │  ├─ ports/
   │  └─ services/
   ├─ domain/
   │  ├─ models/
   │  ├─ value_objects/
   │  └─ errors.py
   ├─ infrastructure/
   │  ├─ persistence/
   │  ├─ external/
   │  └─ clock.py
   └─ bootstrap/
      ├─ config.py
      ├─ container.py
      └─ app_factory.py
```

## 依存方向（必ず守ること）

```
presentation  →  application  →  domain
infrastructure  →  application / domain
bootstrap  →  presentation / infrastructure / application / domain
```

禁止する依存:

| 禁止 | 理由 |
|------|------|
| `domain → application` | domain は最内層 |
| `domain → infrastructure` | 同上 |
| `application → presentation` | 外側への逆依存 |
| `application → infrastructure` | ポートを使い実装詳細を隠す |

## コード生成時のルール（Copilot へ）

| 作成するもの | 配置先 |
|-------------|--------|
| FastAPI router | `presentation/fastapi/routers/` |
| ユースケース | `application/use_cases/` |
| repository interface | `application/ports/` |
| repository 実装 | `infrastructure/persistence/` |
| 業務モデル | `domain/models/` |
| 値オブジェクト | `domain/value_objects/` |
| DI 組み立て | `bootstrap/container.py` または `presentation/fastapi/dependencies.py` |
| OpenAPI 生成モデル | `generated/models/` |

## 実装ルール

1. router に業務ロジックを書かない。router は use case を呼ぶだけ。
2. use case に `fastapi` / `sqlalchemy` を import しない。
3. domain に Pydantic model を入れない。
4. repository interface は `application/ports/` に定義する。
5. repository 実装は `infrastructure/persistence/` に置く。
6. OpenAPI 生成モデルは `generated/` に閉じ込める。domain / application から直接 import しない。
7. DTO ↔ domain model の変換は `presentation/fastapi` 側で行う。
8. app の組み立ては `bootstrap/` に集約する。

## `main.py` は薄く保つ

```python
from <package_name>.bootstrap.app_factory import create_app

app = create_app()
```

## `generated/` の更新コマンド

OpenAPI Spec から Pydantic model を生成する際は `uvx` を使う:

```bash
uvx --from datamodel-code-generator[ruff] datamodel-codegen \
  --input docs/spec/openapi.yaml \
  --input-file-type openapi \
  --output src/<package_name>/generated/models/openapi.py \
  --output-model-type pydantic_v2.BaseModel \
  --formatters ruff-check ruff-format
```

生成モデルの流れ:

```
generated/models  →  presentation/fastapi  →  application/use_cases  →  domain
```

## 手順: 新しいエンドポイントを追加する

1. **domain**: `domain/models/` にエンティティを定義する（Pydantic なし）
2. **application/ports**: repository interface を追加する
3. **application/use_cases**: ユースケースを実装する（FastAPI/SQLAlchemy なし）
4. **infrastructure/persistence**: repository 実装を追加する
5. **presentation/fastapi/routers**: router を作成し use case を呼ぶ
6. **bootstrap/container.py**: DI の配線を追加する
7. **presentation/fastapi/dependencies.py**: `Depends` を更新する

詳細は [レイヤー詳細](./references/layers.md) を参照。

## 手順: 新規プロジェクトのスキャフォールディング

[スキャフォールディング手順](./references/scaffolding.md) を参照。
