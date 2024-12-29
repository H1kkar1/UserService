import uuid
from typing import Sequence

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.liked_manga.schema import LikeManga
from app.liked_manga.model import Liked


async def show_like_by_user_id(
        session: AsyncSession,
        user_id: UUID4,
) -> Sequence[UUID4]:
    query = select(Liked).where(Liked.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def like(
        session: AsyncSession,
        user_id: UUID4,
        manga_id: UUID4,
) -> str:
    """
    Запись манги в понравившиеся
    """
    id = uuid.uuid4()
    new = Liked(
        like_id=id,
        user_id=user_id,
        manga_id=manga_id,
    )
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
