from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from app.liked_manga.service import show_like_by_user_id, like, del_like


like_router = APIRouter(
    prefix="/manga_like",
    tags=["Manga_like"],
)


@like_router.get("/all")
async def all_by_user_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        user_id: UUID4
) -> Sequence[UUID4]:
    result = await show_like_by_user_id(session, user_id)
    manga = [i.manga_id for i in result]
    return manga


@like_router.post("/like_manga")
async def all_by_user_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        user_id: UUID4,
        manga_id: UUID4
) -> str:
    result = await like(session, user_id, manga_id)
    return result


@like_router.delete("/del_manga")
async def all_by_user_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        manga_id: UUID4
) -> str:
    result = await del_like(session, manga_id)
    return result