from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Form, UploadFile
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from app.user.model import User, Role
from app.user.schema import UserRead, UserWrite, UserUpdate

from .service import (get_all_users, get_user_by_id, get_user_by_email,
                     create_user, delete_user, get_current_active_user)

user_router = APIRouter(
    prefix="/user"
)


@user_router.get("/")
async def all(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
) -> Sequence[UserRead]:
    users = await get_all_users(session)
    return users


@user_router.get("/user_by_id")
async def user_by_id(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        user_id: UUID4
) -> UserRead:
    user = await get_user_by_id(session, user_id)
    return user


@user_router.get("/user_by_email")
async def user_by_email(
    session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        email: str,
) -> UserRead:
    user = await get_user_by_email(session, email)
    return user


@user_router.post("/create")
async def create(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        email: Annotated[EmailStr, Form()],
        role: Annotated[Role, Form()],
        photo: UploadFile,

) -> str:
    photo_bytes = await photo.read()
    new = UserWrite(
        username=username,
        password=password,
        email=email,
        role=role,
        photo_name=photo.filename,
        photo_type=photo.content_type,
        photo_data=photo_bytes,
    )
    result = await create_user(session, new)
    return result


@user_router.put("/update")
async def update(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
    user: UserUpdate,
) -> str:
    result = await create_user(session, user)
    return result


@user_router.delete("/delete")
async def delete(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        user_id: UUID4
) -> UserRead:
    result = await delete_user(session, user_id)
    return result

@user_router.get("show_settings")
async def show() -> str:
    rmq