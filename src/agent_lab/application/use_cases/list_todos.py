"""ToDo 一覧取得ユースケース。"""

from dataclasses import dataclass

from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.domain.models.todo import Todo


@dataclass(slots=True)
class ListTodosResult:
    """ToDo 一覧の返却値。"""

    items: list[Todo]
    limit: int
    offset: int
    total: int


class ListTodosUseCase:
    """ToDo 一覧を取得する。"""

    def __init__(self, repository: TodoRepository) -> None:
        """ユースケースを初期化する。

        Args:
            repository: ToDo 永続化ポート。
        """
        self._repository = repository

    async def execute(
        self,
        *,
        completed: bool | None,
        limit: int,
        offset: int,
    ) -> ListTodosResult:
        """ToDo 一覧を取得する。"""
        page = await self._repository.list_todos(
            completed=completed,
            limit=limit,
            offset=offset,
        )
        return ListTodosResult(
            items=page.items,
            limit=limit,
            offset=offset,
            total=page.total,
        )
