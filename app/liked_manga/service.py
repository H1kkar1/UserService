import uuid

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.liked_manga.schema import LikeManga
from app.liked_manga.model import Liked


async def like(
        session: AsyncSession,
        like: LikeManga
) -> str:
    """
    Запись манги в понравившиеся
    """
    id = uuid.uuid4()
    new = Liked(**like.model_dump())
    new.like_id = id
    session.add(new)
    await session.commit()
    return "Добавленно в понравившиеся"


async def del_like(
        session: AsyncSession,
        like_id: UUID4
) -> dict:
    try:
        query = select(Liked).filter(Liked.like_id == like_id)
        like = await session.execute(query)
        if like is None:
            raise HTTPException(status_code=404, detail="Liked not found")
        await session.delete(like)
        await session.commit()
        return {"status_code": 200, "detail": "Запись добавленна в понравившиеся"}
    except Exception as e:
        await session.rollback()
        return {"status_code": 500, "detail": f"{e}"}
