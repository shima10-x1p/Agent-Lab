"""ToDo リポジトリポート。"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from agent_lab.domain.models.todo import Todo


@dataclass(slots=True)
class TodoListPage:
    """ToDo 一覧取得結果。"""

    items: list[Todo]
    total: int


class TodoRepository(ABC):
    """ToDo 永続化の抽象ポート。"""

    @abstractmethod
    async def list_todos(
        self,
        *,
        completed: bool | None,
        limit: int,
        offset: int,
    ) -> TodoListPage:
        """条件に合う ToDo 一覧を返す。"""

    @abstractmethod
    async def get_todo(self, todo_id: str) -> Todo | None:
        """識別子で ToDo を取得する。"""

    @abstractmethod
    async def create_todo(self, todo: Todo) -> Todo:
        """ToDo を保存して返す。"""

    @abstractmethod
    async def update_todo(self, todo: Todo) -> Todo:
        """ToDo を更新して返す。"""

    @abstractmethod
    async def delete_todo(self, todo_id: str) -> bool:
        """ToDo を削除し、削除できた場合に `True` を返す。"""
