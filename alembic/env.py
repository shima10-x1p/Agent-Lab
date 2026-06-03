"""Alembic 実行環境。"""

from __future__ import annotations

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from agent_lab.bootstrap.config import Settings
from agent_lab.infrastructure.persistence.models import Base
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def _to_sync_url(database_url: str) -> str:
    """Alembic 用に同期ドライバー URL へ変換する。"""
    return database_url.replace("+aiosqlite", "", 1)


def run_migrations_offline() -> None:
    """オフラインマイグレーションを実行する。"""
    url = _to_sync_url(Settings().database_url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """同期接続を使ってマイグレーションを実行する。"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """オンラインマイグレーションを実行する。"""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = Settings().database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
