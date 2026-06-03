"""FastAPI 用の依存解決定義。"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from agent_lab.application.ports.clock import ClockPort
from agent_lab.application.ports.todo_repository import TodoRepository
from agent_lab.application.use_cases.create_todo import CreateTodoUseCase
from agent_lab.application.use_cases.delete_todo import DeleteTodoUseCase
from agent_lab.application.use_cases.get_todo import GetTodoUseCase
from agent_lab.application.use_cases.list_todos import ListTodosUseCase
from agent_lab.application.use_cases.update_todo import UpdateTodoUseCase
from agent_lab.bootstrap.config import Settings
from agent_lab.bootstrap.container import Container
from agent_lab.infrastructure.persistence.todo_repository import (
    SqlAlchemyTodoRepository,
)


def get_container(request: Request) -> Container:
    """アプリケーションコンテナを返す。"""
    return request.app.state.container


ContainerDependency = Annotated[Container, Depends(get_container)]


def get_settings(container: ContainerDependency) -> Settings:
    """アプリケーション設定を返す。"""
    return container.settings


def get_clock(container: ContainerDependency) -> ClockPort:
    """Clock 実装を返す。"""
    return container.clock


async def get_session(
    container: ContainerDependency,
) -> AsyncIterator[AsyncSession]:
    """リクエスト単位の DB セッションを返す。"""
    async with container.session_factory() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]


def get_todo_repository(
    session: SessionDependency,
) -> TodoRepository:
    """ToDo リポジトリ実装を返す。"""
    return SqlAlchemyTodoRepository(session)


RepositoryDependency = Annotated[TodoRepository, Depends(get_todo_repository)]
ClockDependency = Annotated[ClockPort, Depends(get_clock)]


def get_list_todos_use_case(
    repository: RepositoryDependency,
) -> ListTodosUseCase:
    """一覧取得ユースケースを返す。"""
    return ListTodosUseCase(repository)


def get_get_todo_use_case(
    repository: RepositoryDependency,
) -> GetTodoUseCase:
    """単一取得ユースケースを返す。"""
    return GetTodoUseCase(repository)


def get_create_todo_use_case(
    repository: RepositoryDependency,
    clock: ClockDependency,
) -> CreateTodoUseCase:
    """作成ユースケースを返す。"""
    return CreateTodoUseCase(repository, clock)


def get_update_todo_use_case(
    repository: RepositoryDependency,
    clock: ClockDependency,
) -> UpdateTodoUseCase:
    """更新ユースケースを返す。"""
    return UpdateTodoUseCase(repository, clock)


def get_delete_todo_use_case(
    repository: RepositoryDependency,
) -> DeleteTodoUseCase:
    """削除ユースケースを返す。"""
    return DeleteTodoUseCase(repository)
