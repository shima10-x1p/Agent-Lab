"""ToDo ドメインモデル。"""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(slots=True)
class Todo:
    """ToDo エンティティ。"""

    id: str
    title: str
    description: str | None
    completed: bool
    due_date: date | None
    created_at: datetime
    updated_at: datetime
