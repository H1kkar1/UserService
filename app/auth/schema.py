from pydantic import BaseModel
from typing_extensions import Optional


class Login(BaseModel):
    username: Optional[str]
    password: str


class Authorization(BaseModel):
    email: str
    password: str
    username: str


class Recovery(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
