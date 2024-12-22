import hashlib
import uuid
from datetime import timezone, datetime, timedelta
from typing import Annotated, Sequence, Type

import jwt
from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import UUID4, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import TokenData, Login
from app.config import settings
from app.user.model import User
from app.user.schema import UserRead, UserWrite, UserUpdate

from app.rabbitmq import rmq


hash_obj = hashlib.sha256()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_all_users(
        session: AsyncSession
) -> Sequence[User]:
    """
    Получение всех пользователей
    """
    query = select(User)
    result = await session.scalars(query)
    return result.all()


async def get_user_by_id(
        session: AsyncSession,
        user_id: UUID4,
) -> UserRead:
    """
    Получить только 1 по id
    """
    query = select(User).filter(User.id == user_id)
    result = await session.execute(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = result.scalars().first()
    photo = bytes(user.photo)
    new = UserRead(
        username=user.username,
        email=user.email,
        role=user.role,
        photo=photo,
        liked_manga=user.liked_manga,
        your_works=user.your_works,
        date=user.date,
    )
    return new


async def get_user_by_email(
        session: AsyncSession,
        email: EmailStr,
) -> User:
    """
    Получить пользователя по email
    Пригодиться в фильтрах посика
    """
    query = select(User).filter(User.email == email.encode("utf-8"))
    result = await session.execute(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result.scalars().first()


async def get_user_by_name(
        session: AsyncSession,
        username: str,
) -> User:
    """
    Получить пользователя по email
    Пригодиться в фильтрах посика
    """
    query = select(User).filter(User.username == username)
    result = await session.execute(query)
    # TODO Обратиться к S3 хранилищу для картинки профиля
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result.scalars().first()


async def create_user(
        session: AsyncSession,
        user: UserWrite,
) -> str:
    """
    Создание пользователя
    """
    try:
        id = uuid.uuid4()
        jwt_token = create_access_token({'id': str(id)})
        rmq.put_user_profile_photo(user.photo_name, user.photo_type, user.photo_data)
        new = User(
            id=id,
            username=user.username,
            password=get_password_hash(user.password),
            email=user.email,
            photo=user.photo_name,
            liked_manga=None,
            your_works=None,
            date=None,
            token=jwt_token,

        )
        session.add(new)
        await session.commit()
        return jwt_token
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User not created, {e}")


async def update_user(
        session: AsyncSession,
        user_update: UserUpdate,
) -> User:
    """
    Обновить данные пользователя
    """
    result = await session.execute(select(User).filter(User.id == user_update.id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.password = get_password_hash(user.password)
    await session.commit()
    return user


async def delete_user(
        session: AsyncSession,
        id: UUID4,
) -> str:
    try:
        user = await get_user_by_id(session, id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
        return "Пользователь успешно удалён"
    except Exception as e:
        raise HTTPException(status_code=400, detail="Fail deleted")


def verify_password(plain_password, hashed_password):
    return True if hashed_password == hashlib.sha256(plain_password) else False


def get_password_hash(password: str) -> str:
    hash_obj.update(password.encode('utf-8'))
    hex_dig = hash_obj.hexdigest()
    return hex_dig


def authenticate_user(
        session: AsyncSession,
        login: Login
):
    user = get_user_by_name(session, login.username)
    if not user:
        return False
    if not verify_password(login.password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt.secret, algorithm=settings.jwt.algorithm)
    return encoded_jwt


async def get_current_user(
        session: AsyncSession,
        token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt.secret, algorithms=[settings.jwt.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_name(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def show_settings():
    return {
        "rmq_port": settings.rmq.port,
        "rmq_host": settings.rmq.host,
    }