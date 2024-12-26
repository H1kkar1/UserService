from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Form, UploadFile
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_helper
from app.user.model import User, Role
from app.user.schema import UserRead, UserWrite, UserUpdate
from app.user.model import Role

from .service import (get_all_users, get_user_by_id, get_user_by_email,
                     create_user, delete_user, get_current_active_user, get_user_by_name)

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
        username: str,
) -> UserRead:
    user = await get_user_by_name(session, username=username)
    return user


@user_router.get("/user_by_username")
async def user_by_username(
    session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        name: str,
) -> UserRead:
    user = await get_user_by_name(session, name)
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
        filename=photo.filename.split('.')[1],
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
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    role: Annotated[Role, Form()],
    image: UploadFile,
) -> str:
    photo = await image.read()
    new_user = UserWrite(
        username=username,
        email=email,
        role=role,
        photo_type=image.content_type,
        photo_data=photo,
    )
    result = await create_user(session, new_user)
    return result


@user_router.delete("/delete")
async def delete(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.sessionDep)
        ],
        user_id: UUID4
) -> str:
    result = await delete_user(session, user_id)
    return result
