# generated/

このディレクトリは OpenAPI 仕様から生成した DTO を置く場所です。

手動編集は避け、必要な場合は生成コマンドを再実行してください。

## 更新コマンド

`uvx --from datamodel-code-generator[ruff] datamodel-codegen --input docs/spec/openapi.yaml --input-file-type openapi --output src/agent_lab/generated/models/openapi.py --output-model-type pydantic_v2.BaseModel --formatters ruff-check ruff-format`
