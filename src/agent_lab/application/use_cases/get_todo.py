"""ToDo 取得ユースケース。"""

from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.domain.errors import TodoNotFoundError
from agent_lab.domain.models.todo import Todo


class GetTodoUseCase:
    """ToDo を 1 件取得する。"""

    def __init__(self, repository: TodoRepository) -> None:
        """ユースケースを初期化する。

        Args:
            repository: ToDo 永続化ポート。
        """
        self._repository = repository

    async def execute(self, *, todo_id: str) -> Todo:
        """識別子で ToDo を取得する。"""
        todo = await self._repository.get_todo(todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        return todo
