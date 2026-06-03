# スキャフォールディング手順

新規プロジェクトでヘキサゴナルアーキテクチャのディレクトリ構成を作成する手順。

## 前提

- パッケージ名が決まっていること（例: `todo_api`）
- `src/` ディレクトリをルートに使う構成

---

## 手順

### 1. パッケージ名を確認する

`pyproject.toml` の `[project].name` または `[tool.hatch.build.targets.wheel]` を参照して決定する。
未定の場合は ユーザーに確認する。

### 2. ディレクトリ・ファイルを作成する

`<package_name>` を実際の名前に置き換えて実行する:

```powershell
$pkg = "<package_name>"
$base = "src/$pkg"

# 全ディレクトリを作成
@(
    "$base/generated/apis",
    "$base/generated/models",
    "$base/presentation/fastapi/routers",
    "$base/application/use_cases",
    "$base/application/ports",
    "$base/application/services",
    "$base/domain/models",
    "$base/domain/value_objects",
    "$base/infrastructure/persistence",
    "$base/infrastructure/external",
    "$base/bootstrap"
) | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null }

# __init__.py を配置
@(
    "$base",
    "$base/generated",
    "$base/generated/apis",
    "$base/generated/models",
    "$base/presentation",
    "$base/presentation/fastapi",
    "$base/presentation/fastapi/routers",
    "$base/application",
    "$base/application/use_cases",
    "$base/application/ports",
    "$base/application/services",
    "$base/domain",
    "$base/domain/models",
    "$base/domain/value_objects",
    "$base/infrastructure",
    "$base/infrastructure/persistence",
    "$base/infrastructure/external",
    "$base/bootstrap"
) | ForEach-Object { New-Item -ItemType File -Path "$_/__init__.py" -Force | Out-Null }
```

### 3. スタブファイルを作成する

以下のファイルを作成する（最低限の内容で可）:

| ファイル | 内容 |
|--------|------|
| `src/<pkg>/main.py` | `app = create_app()` のみ |
| `src/<pkg>/domain/errors.py` | ドメインエラーの基底クラス |
| `src/<pkg>/infrastructure/clock.py` | `ClockPort` 実装 |
| `src/<pkg>/bootstrap/config.py` | `Settings` クラス（pydantic-settings） |
| `src/<pkg>/bootstrap/container.py` | DI 配線（最初は空でよい） |
| `src/<pkg>/bootstrap/app_factory.py` | `create_app()` 関数 |
| `src/<pkg>/presentation/fastapi/dependencies.py` | `Depends` 定義 |
| `src/<pkg>/presentation/fastapi/error_handlers.py` | exception handler 登録 |
| `src/<pkg>/generated/README.md` | 自動生成ファイルの注意書き |

#### `main.py`

```python
from <package_name>.bootstrap.app_factory import create_app

app = create_app()
```

#### `domain/errors.py`

```python
class DomainError(Exception):
    """ドメインエラーの基底クラス。"""
```

#### `bootstrap/app_factory.py`

```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI()
    return app
```

#### `generated/README.md`

```markdown
# generated/

このディレクトリは自動生成されたコードを置く場所です。

手動で編集しないでください。

## 更新方法

```bash
uvx --from datamodel-code-generator[ruff] datamodel-codegen \
  --input docs/spec/openapi.yaml \
  --input-file-type openapi \
  --output src/<package_name>/generated/models/openapi.py \
  --output-model-type pydantic_v2.BaseModel \
  --formatters ruff-check ruff-format
```
```

---

## 確認チェックリスト

- [ ] `src/<pkg>/__init__.py` が存在する
- [ ] `main.py` が `create_app()` を呼ぶだけになっている
- [ ] `domain/` に FastAPI / Pydantic / SQLAlchemy の import がない
- [ ] `application/` に FastAPI / SQLAlchemy の import がない
- [ ] `generated/` に README.md が存在し、生成コマンドが記載されている
- [ ] `bootstrap/app_factory.py` が router を組み込む責務を持っている
