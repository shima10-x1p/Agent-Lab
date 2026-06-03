"""ToDo 作成ユースケース。"""

from datetime import date
from uuid import uuid4

from agent_lab.application.ports.clock import ClockPort
from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.domain.models.todo import Todo


class CreateTodoUseCase:
    """ToDo を作成する。"""

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
        title: str,
        description: str | None,
        due_date: date | None,
    ) -> Todo:
        """新しい ToDo を作成する。
        
        Args:
            title: ToDo のタイトル。
            description: ToDo の説明。
            due_date: ToDo の期限日。
        
        Returns:
            作成された ToDo。
        """
        now = self._clock.now()
        todo = Todo(
            id=str(uuid4()),
            title=title,
            description=description,
            completed=False,
            due_date=due_date,
            created_at=now,
            updated_at=now,
        )
        return await self._repository.create_todo(todo)
