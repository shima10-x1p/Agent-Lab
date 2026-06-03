"""ToDo API ルーター。"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from agent_lab.application.use_cases.create_todo import CreateTodoUseCase
from agent_lab.application.use_cases.delete_todo import DeleteTodoUseCase
from agent_lab.application.use_cases.get_todo import GetTodoUseCase
from agent_lab.application.use_cases.list_todos import ListTodosUseCase
from agent_lab.application.use_cases.update_todo import UpdateTodoUseCase
from agent_lab.domain.models.todo import Todo as DomainTodo
from agent_lab.generated.models.openapi import (
    CreateTodoRequest,
    Error,
    Todo,
    UpdateTodoRequest,
)
from agent_lab.presentation.fastapi.dependencies import (
    get_create_todo_use_case,
    get_delete_todo_use_case,
    get_get_todo_use_case,
    get_list_todos_use_case,
    get_update_todo_use_case,
)
from agent_lab.presentation.fastapi.schemas import TodoListResponse

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get(
    "",
    operation_id="listTodos",
    response_model=TodoListResponse,
    responses={400: {"model": Error}},
)
async def list_todos(
    use_case: Annotated[ListTodosUseCase, Depends(get_list_todos_use_case)],
    completed: Annotated[
        bool | None,
        Query(
            description="完了状態で絞り込みます。指定しない場合はすべてのToDoを返します。",
        ),
    ] = None,
    limit: Annotated[
        int,
        Query(ge=1, le=100, description="取得する件数の上限です。"),
    ] = 20,
    offset: Annotated[
        int,
        Query(ge=0, description="取得開始位置です。"),
    ] = 0,
) -> TodoListResponse:
    """ToDo 一覧を取得する。"""
    result = await use_case.execute(completed=completed, limit=limit, offset=offset)
    return TodoListResponse(
        items=[_to_openapi_todo(item) for item in result.items],
        limit=result.limit,
        offset=result.offset,
        total=result.total,
    )


@router.post(
    "",
    operation_id="createTodo",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "headers": {
                "Location": {
                    "description": "作成されたToDoのURLです。",
                    "schema": {"type": "string"},
                }
            }
        },
        400: {"model": Error},
    },
)
async def create_todo(
    body: CreateTodoRequest,
    response: Response,
    use_case: Annotated[CreateTodoUseCase, Depends(get_create_todo_use_case)],
) -> Todo:
    """ToDo を作成する。"""
    todo = await use_case.execute(
        title=body.title,
        description=body.description,
        due_date=body.dueDate,
    )
    response.headers["Location"] = f"/todos/{todo.id}"
    return _to_openapi_todo(todo)


@router.get(
    "/{todoId}",
    operation_id="getTodo",
    response_model=Todo,
    responses={404: {"model": Error}},
)
async def get_todo(
    todoId: Annotated[str, Path(description="ToDoを識別するIDです。")],
    use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)],
) -> Todo:
    """ToDo を 1 件取得する。"""
    todo = await use_case.execute(todo_id=todoId)
    return _to_openapi_todo(todo)


@router.put(
    "/{todoId}",
    operation_id="updateTodo",
    response_model=Todo,
    responses={400: {"model": Error}, 404: {"model": Error}},
)
async def update_todo(
    todoId: Annotated[str, Path(description="ToDoを識別するIDです。")],
    body: UpdateTodoRequest,
    use_case: Annotated[UpdateTodoUseCase, Depends(get_update_todo_use_case)],
) -> Todo:
    """ToDo を全体置換で更新する。"""
    todo = await use_case.execute(
        todo_id=todoId,
        title=body.title,
        description=body.description,
        completed=body.completed,
        due_date=body.dueDate,
    )
    return _to_openapi_todo(todo)


@router.delete(
    "/{todoId}",
    operation_id="deleteTodo",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": Error}},
)
async def delete_todo(
    todoId: Annotated[str, Path(description="ToDoを識別するIDです。")],
    use_case: Annotated[DeleteTodoUseCase, Depends(get_delete_todo_use_case)],
) -> Response:
    """ToDo を削除する。"""
    await use_case.execute(todo_id=todoId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _to_openapi_todo(todo: DomainTodo) -> Todo:
    """ドメインモデルを OpenAPI DTO へ変換する。"""
    return Todo(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        dueDate=todo.due_date,
        createdAt=todo.created_at,
        updatedAt=todo.updated_at,
    )
