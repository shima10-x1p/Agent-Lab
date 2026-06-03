"""ToDo 削除ユースケース。"""

from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.domain.errors import TodoNotFoundError


class DeleteTodoUseCase:
    """ToDo を削除する。"""

    def __init__(self, repository: TodoRepository) -> None:
        """ユースケースを初期化する。

        Args:
            repository: ToDo 永続化ポート。
        """
        self._repository = repository

    async def execute(self, *, todo_id: str) -> None:
        """識別子で ToDo を削除する。"""
        deleted = await self._repository.delete_todo(todo_id)
        if not deleted:
            raise TodoNotFoundError(todo_id)
