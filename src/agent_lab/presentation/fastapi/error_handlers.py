"""FastAPI 用の例外ハンドラー。"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from agent_lab.domain.errors import TodoNotFoundError
from agent_lab.generated.models.openapi import Error

logger = logging.getLogger(__name__)


def register_handlers(app: FastAPI) -> None:
    """FastAPI アプリケーションへ例外ハンドラーを登録する。"""

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        del request
        payload = Error(
            code="bad_request",
            message="リクエスト内容が不正です。",
            details=[
                {
                    "field": _format_field_name(error.get("loc", ())),
                    "message": error.get("msg", "不正な入力です。"),
                }
                for error in exc.errors()
            ],
        )
        return JSONResponse(
            status_code=400,
            content=payload.model_dump(mode="json", exclude_none=True),
        )

    @app.exception_handler(TodoNotFoundError)
    async def handle_todo_not_found(
        request: Request,
        exc: TodoNotFoundError,
    ) -> JSONResponse:
        del request
        payload = Error(code="not_found", message=str(exc))
        return JSONResponse(
            status_code=404,
            content=payload.model_dump(mode="json", exclude_none=True),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unhandled error on %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        payload = Error(
            code="internal_server_error",
            message="内部エラーが発生しました。",
        )
        return JSONResponse(
            status_code=500,
            content=payload.model_dump(mode="json", exclude_none=True),
        )


def _format_field_name(location: tuple[Any, ...]) -> str:
    """FastAPI の location 情報を項目名へ変換する。"""
    parts = [str(part) for part in location if part not in {"body", "query", "path"}]
    if not parts:
        return "request"
    return ".".join(parts)
