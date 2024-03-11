from fastapi import APIRouter

from app.base.db import init_db

router = APIRouter(tags=["Tooling"])


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}


@router.post("/initdb")
async def init_db_route() -> None:
    await init_db()


# @router.get("/env")
# async def env() -> None:
#     return settings
