"""アプリケーション設定。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数から読み込むアプリケーション設定。"""

    app_name: str = "ToDo API"
    app_version: str = "1.0.0"
    database_url: str = "sqlite+aiosqlite:///./todo_api.db"
    auto_create_schema: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TODO_API_",
        extra="ignore",
    )
