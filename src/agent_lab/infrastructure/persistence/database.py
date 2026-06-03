"""データベース接続ユーティリティ。"""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from agent_lab.infrastructure.persistence.models import Base


def create_engine_and_session_factory(
    database_url: str,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """エンジンとセッションファクトリを生成する。
    
    Args:
        database_url: データベース接続 URL。
    
    Returns:
        エンジンとセッションファクトリのタプル。
    """
    engine = create_async_engine(database_url, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_factory


async def create_schema(engine: AsyncEngine) -> None:
    """メタデータからスキーマを作成する。
    
    Args:
        engine: スキーマを作成するエンジン。
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def dispose_engine(engine: AsyncEngine) -> None:
    """エンジンを破棄する。
    
    Args:
        engine: 破棄するエンジン。
    """
    await engine.dispose()
