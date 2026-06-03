"""ToDo リポジトリの SQLAlchemy 実装。"""

from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from agent_lab.application.ports.todo_repository import TodoListPage, TodoRepository
from agent_lab.domain.models.todo import Todo
from agent_lab.infrastructure.persistence.models import TodoRow


class SqlAlchemyTodoRepository(TodoRepository):
    """ToDo リポジトリの SQLAlchemy 実装。"""

    def __init__(self, session: AsyncSession) -> None:
        """リポジトリを初期化する。

        Args:
            session: 非同期 SQLAlchemy セッション。
        """
        self._session = session

    async def list_todos(
        self,
        *,
        completed: bool | None,
        limit: int,
        offset: int,
    ) -> TodoListPage:
        """条件に合う ToDo 一覧を返す。"""
        total = int((await self._session.scalar(select(func.count(TodoRow.id)))) or 0)

        query = select(TodoRow)
        if completed is not None:
            query = query.where(TodoRow.completed.is_(completed))
        query = query.order_by(TodoRow.created_at.desc()).limit(limit).offset(offset)

        rows = list((await self._session.scalars(query)).all())
        return TodoListPage(
            items=[self._to_domain_model(row) for row in rows],
            total=total,
        )

    async def get_todo(self, todo_id: str) -> Todo | None:
        """識別子で ToDo を取得する。"""
        row = await self._session.get(TodoRow, todo_id)
        if row is None:
            return None
        return self._to_domain_model(row)

    async def create_todo(self, todo: Todo) -> Todo:
        """ToDo を保存して返す。"""
        row = TodoRow(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            due_date=todo.due_date,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        self._session.add(row)
        await self._session.commit()
        return self._to_domain_model(row)

    async def update_todo(self, todo: Todo) -> Todo:
        """ToDo を更新して返す。"""
        row = await self._session.get(TodoRow, todo.id)
        if row is None:
            raise ValueError(f"ToDo not found: {todo.id}")

        row.title = todo.title
        row.description = todo.description
        row.completed = todo.completed
        row.due_date = todo.due_date
        row.updated_at = todo.updated_at

        await self._session.commit()
        return self._to_domain_model(row)

    async def delete_todo(self, todo_id: str) -> bool:
        """ToDo を削除し、削除できた場合に `True` を返す。"""
        row = await self._session.get(TodoRow, todo_id)
        if row is None:
            return False

        await self._session.delete(row)
        await self._session.commit()
        return True

    def _to_domain_model(self, row: TodoRow) -> Todo:
        """ORM モデルをドメインモデルへ変換する。"""
        return Todo(
            id=row.id,
            title=row.title,
            description=row.description,
            completed=row.completed,
            due_date=row.due_date,
            created_at=self._normalize_datetime(row.created_at),
            updated_at=self._normalize_datetime(row.updated_at),
        )

    def _normalize_datetime(self, value: datetime) -> datetime:
        """SQLite から返る日時を UTC aware に正規化する。"""
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
