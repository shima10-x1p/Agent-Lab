# レイヤー詳細

## `domain/`

業務ルールの中心。外部ライブラリに依存しない。

| 置くもの | 例 |
|---------|-----|
| エンティティ | `domain/models/user.py` |
| 値オブジェクト | `domain/value_objects/email.py` |
| ドメインエラー | `domain/errors.py` |
| ドメインロジック（純粋な計算） | — |

**禁止 import**: `fastapi`, `pydantic`, `sqlalchemy`, `httpx`

### エンティティの例

```python
# domain/models/user.py
from dataclasses import dataclass
from .value_objects.email import Email

@dataclass
class User:
    id: int
    email: Email
    name: str
```

### 値オブジェクトの例

```python
# domain/value_objects/email.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")
```

---

## `application/`

「何をするか」を表現する層。domain にのみ依存する。

| 置くもの | 例 |
|---------|-----|
| ユースケース | `application/use_cases/create_user.py` |
| repository interface | `application/ports/user_repository.py` |
| transaction interface | `application/ports/transaction.py` |
| application service | `application/services/` |

**禁止 import**: `fastapi`, `sqlalchemy`, `httpx`

### repository interface の例

```python
# application/ports/user_repository.py
from abc import ABC, abstractmethod
from domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...
```

### ユースケースの例

```python
# application/use_cases/create_user.py
from domain.models.user import User
from domain.value_objects.email import Email
from application.ports.user_repository import UserRepository

class CreateUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def execute(self, name: str, email: str) -> User:
        user = User(id=0, email=Email(email), name=name)
        await self._repository.save(user)
        return user
```

---

## `presentation/fastapi/`

HTTP の入口。FastAPI の詳細をここに閉じ込める。

| 置くもの | 例 |
|---------|-----|
| FastAPI router | `presentation/fastapi/routers/users.py` |
| Depends | `presentation/fastapi/dependencies.py` |
| request/response mapping | router 内 |
| exception handler | `presentation/fastapi/error_handlers.py` |

**ルール**: router は use case を呼ぶだけ。業務ロジックを書かない。

### router の例

```python
# presentation/fastapi/routers/users.py
from fastapi import APIRouter, Depends
from generated.models.openapi import CreateUserRequest, UserResponse
from application.use_cases.create_user import CreateUserUseCase
from presentation.fastapi.dependencies import get_create_user_use_case

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    body: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:
    # DTO → use case へ必要な値だけ渡す
    user = await use_case.execute(name=body.name, email=body.email)
    # domain model → response DTO へ変換
    return UserResponse(id=user.id, name=user.name, email=user.email.value)
```

---

## `infrastructure/`

技術詳細の実装。application の port を実装する。

| 置くもの | 例 |
|---------|-----|
| SQLAlchemy model | `infrastructure/persistence/models.py` |
| repository 実装 | `infrastructure/persistence/user_repository.py` |
| 外部 API client | `infrastructure/external/payment_client.py` |
| clock 実装 | `infrastructure/clock.py` |

### repository 実装の例

```python
# infrastructure/persistence/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from application.ports.user_repository import UserRepository
from domain.models.user import User
from domain.value_objects.email import Email
from infrastructure.persistence.models import UserRow

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, user_id: int) -> User | None:
        row = await self._session.get(UserRow, user_id)
        if row is None:
            return None
        return User(id=row.id, email=Email(row.email), name=row.name)

    async def save(self, user: User) -> None:
        row = UserRow(id=user.id, email=user.email.value, name=user.name)
        self._session.add(row)
        await self._session.flush()
```

---

## `bootstrap/`

アプリ全体の組み立て場所。

| 置くもの | 例 |
|---------|-----|
| 設定読み込み | `bootstrap/config.py` |
| DI container | `bootstrap/container.py` |
| FastAPI app factory | `bootstrap/app_factory.py` |

### app_factory の例

```python
# bootstrap/app_factory.py
from fastapi import FastAPI
from presentation.fastapi.routers import users
from presentation.fastapi.error_handlers import register_handlers

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)
    register_handlers(app)
    return app
```
