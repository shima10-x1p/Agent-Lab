"""ToDo API の統合テスト。"""

from fastapi.testclient import TestClient

from agent_lab.bootstrap.app_factory import create_app
from agent_lab.bootstrap.config import Settings


def test_healthz_is_available(client: TestClient) -> None:
    """ヘルスチェックが利用できることを確認する。"""
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_todo_crud_flow(client: TestClient) -> None:
    """作成から削除までの基本フローを確認する。"""
    create_response = client.post(
        "/todos",
        json={
            "title": "買い物に行く",
            "description": "牛乳と卵を買う",
            "dueDate": "2026-06-10",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    todo_id = created["id"]
    assert create_response.headers["Location"] == f"/todos/{todo_id}"
    assert created["completed"] is False

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == todo_id

    update_response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "買い物に行く",
            "description": "牛乳、卵、パンを買う",
            "completed": True,
            "dueDate": "2026-06-10",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["createdAt"] == created["createdAt"]

    list_response = client.get("/todos", params={"completed": True})
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert len(list_response.json()["items"]) == 1

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_response = client.get(f"/todos/{todo_id}")
    assert missing_response.status_code == 404
    assert missing_response.json()["code"] == "not_found"


def test_validation_errors_are_normalized_to_400(client: TestClient) -> None:
    """バリデーションエラーが 400 に正規化されることを確認する。"""
    response = client.post("/todos", json={})

    assert response.status_code == 400
    payload = response.json()
    assert payload["code"] == "bad_request"
    assert payload["message"] == "リクエスト内容が不正です。"
    assert payload["details"]


def test_total_is_returned_before_filtering(client: TestClient) -> None:
    """total がフィルタ前件数を返すことを確認する。"""
    first = client.post("/todos", json={"title": "未完了"})
    second = client.post("/todos", json={"title": "完了予定"})
    todo_id = second.json()["id"]

    client.put(
        f"/todos/{todo_id}",
        json={
            "title": "完了予定",
            "description": None,
            "completed": True,
            "dueDate": None,
        },
    )

    response = client.get("/todos", params={"completed": True})

    assert first.status_code == 201
    assert second.status_code == 201
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["items"]) == 1


def test_openapi_includes_expected_operation_ids(tmp_path) -> None:
    """OpenAPI に期待する operationId が含まれることを確認する。"""
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'openapi.db'}",
        auto_create_schema=True,
    )
    app = create_app(settings)
    schema = app.openapi()

    assert "/healthz" not in schema["paths"]
    assert schema["paths"]["/todos"]["get"]["operationId"] == "listTodos"
    assert schema["paths"]["/todos"]["post"]["operationId"] == "createTodo"
    assert schema["paths"]["/todos/{todoId}"]["get"]["operationId"] == "getTodo"
    assert schema["paths"]["/todos/{todoId}"]["put"]["operationId"] == "updateTodo"
    assert schema["paths"]["/todos/{todoId}"]["delete"]["operationId"] == "deleteTodo"
