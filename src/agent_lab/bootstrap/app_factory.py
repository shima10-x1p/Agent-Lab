"""FastAPI アプリケーションファクトリ。"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from agent_lab.bootstrap.config import Settings
from agent_lab.bootstrap.container import (
    build_container,
    initialize_container,
    shutdown_container,
)
from agent_lab.presentation.fastapi.error_handlers import register_handlers
from agent_lab.presentation.fastapi.routers import health, todos

_DESCRIPTION = (
    "ToDoを管理するためのシンプルなAPIです。\n"
    "認証認可は不要で、ToDoの取得、作成、更新、削除を行えます。"
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """FastAPI アプリケーションを生成する。

    Args:
        settings: 起動時に使うアプリケーション設定。

    Returns:
        構成済みの FastAPI アプリケーション。
    """
    active_settings = settings or Settings()
    container = build_container(active_settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """アプリケーションの起動と終了に伴うリソースを管理する。

        Args:
            app: 起動中の FastAPI アプリケーション。

        Yields:
            アプリケーション稼働中の制御を返す。
        """
        app.state.container = container
        await initialize_container(container)
        try:
            yield
        finally:
            await shutdown_container(container)

    app = FastAPI(
        title=active_settings.app_name,
        version=active_settings.app_version,
        description=_DESCRIPTION,
        lifespan=lifespan,
        openapi_tags=[{"name": "Todos", "description": "ToDoの操作"}],
    )
    register_handlers(app)
    app.include_router(health.router)
    app.include_router(todos.router)
    return app
