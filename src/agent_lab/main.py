"""ASGI アプリケーションのエントリーポイント。"""

from agent_lab.bootstrap.app_factory import create_app

app = create_app()
