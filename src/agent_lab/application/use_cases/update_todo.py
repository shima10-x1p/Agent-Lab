"""ToDo 更新ユースケース。"""

from datetime import date

from agent_lab.application.ports.clock import ClockPort
from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.domain.errors import TodoNotFoundError
from agent_lab.domain.models.todo import Todo


class UpdateTodoUseCase:
    """ToDo を全体置換で更新する。"""

    def __init__(self, repository: TodoRepository, clock: ClockPort) -> None:
        """ユースケースを初期化する。

        Args:
            repository: ToDo 永続化ポート。
            clock: 現在時刻を返すポート。
        """
        self._repository = repository
        self._clock = clock

    async def execute(
        self,
        *,
        todo_id: str,
        title: str,
        description: str | None,
        completed: bool,
        due_date: date | None,
    ) -> Todo:
        """ToDo を全体置換で更新する。"""
        current = await self._repository.get_todo(todo_id)
        if current is None:
            raise TodoNotFoundError(todo_id)

        updated = Todo(
            id=current.id,
            title=title,
            description=description,
            completed=completed,
            due_date=due_date,
            created_at=current.created_at,
            updated_at=self._clock.now(),
        )
        return await self._repository.update_todo(updated)
