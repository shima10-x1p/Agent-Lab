"""FastAPI 用レスポンススキーマ。"""

from pydantic import BaseModel, Field

from agent_lab.generated.models.openapi import Todo


class TodoListResponse(BaseModel):
    """ToDo 一覧レスポンス。"""

    items: list[Todo] = Field(..., description="ToDoの一覧です。")
    limit: int = Field(..., description="取得件数の上限です。", examples=[20])
    offset: int = Field(..., description="取得開始位置です。", examples=[0])
    total: int = Field(..., description="ToDoの総件数です。", examples=[1])
