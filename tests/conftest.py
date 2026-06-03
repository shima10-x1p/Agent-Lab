"""テスト共通フィクスチャ。"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from agent_lab.bootstrap.app_factory import create_app
from agent_lab.bootstrap.config import Settings


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    """テスト用クライアントを返す。"""
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        auto_create_schema=True,
    )
    app = create_app(settings)

    with TestClient(app) as test_client:
        yield test_client
