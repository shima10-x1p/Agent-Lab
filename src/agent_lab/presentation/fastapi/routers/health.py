"""ヘルスチェック用ルーター。"""

from fastapi import APIRouter

router = APIRouter(include_in_schema=False)


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """サービスの生存確認を返す。"""
    return {"status": "ok"}
