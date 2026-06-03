"""依存関係の組み立て。"""

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from agent_lab.application.ports.clock import ClockPort
from agent_lab.bootstrap.config import Settings
from agent_lab.infrastructure.clock import UtcClock
from agent_lab.infrastructure.persistence.database import (
    create_engine_and_session_factory,
    create_schema,
    dispose_engine,
)


@dataclass(slots=True)
class Container:
    """アプリケーション全体で共有する依存関係。"""

    settings: Settings
    clock: ClockPort
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]


def build_container(settings: Settings | None = None) -> Container:
    """依存関係を束ねたコンテナを構築する。
    
    Args:
        settings: 起動時に使うアプリケーション設定。指定しない場合はデフォルト設定。
    
    Returns:
        構成されたコンテナ。
    """
    active_settings = settings or Settings()
    engine, session_factory = create_engine_and_session_factory(
        active_settings.database_url,
    )
    return Container(
        settings=active_settings,
        clock=UtcClock(),
        engine=engine,
        session_factory=session_factory,
    )


async def initialize_container(container: Container) -> None:
    """コンテナ初期化時に必要なセットアップを行う。
    
    Args:
        container: 初期化するコンテナ。
    """
    if container.settings.auto_create_schema:
        await create_schema(container.engine)


async def shutdown_container(container: Container) -> None:
    """コンテナが保持するリソースを解放する。
    
    Args:
        container: 解放するコンテナ。
    """
    await dispose_engine(container.engine)
