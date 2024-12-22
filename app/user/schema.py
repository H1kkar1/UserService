from datetime import datetime

from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, Annotated

from app.user.model import Role


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role
    photo: bytes
    liked_manga: Optional[UUID4]
    your_works: Optional[UUID4]
    date: datetime


class UserRead(UserBase):
    pass


class UserWrite(BaseModel):
    username: str
    email: str
    password: str
    role: Role
    photo_name: Optional[str]
    photo_type: Optional[str]
    photo_data: Optional[bytes]


class UserUpdate(BaseModel):
    id: UUID4
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    photo: Optional[UploadFile]
