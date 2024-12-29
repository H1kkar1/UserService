import enum
from datetime import date
from sqlalchemy import Column, String, Table, Uuid, Date, Enum
from app.db import db_helper


class Role(enum.Enum):
    """
    Пояснений не будет (см. файл Роли)
    """
    READER = "Читатель"
    PAINTER = "Художник"
    CONTRIBUTOR = "Бета"
    PRINTER = "Тайпер"
    EDITOR = "Редактор"


user = Table(
    "user",
    db_helper.metadata_obj,
    Column("id", Uuid, primary_key=True, nullable=False, unique=True),
    Column("username", String(128), nullable=False, unique=True),
    Column("password", String(64), nullable=False),
    Column("email", String(128), nullable=False),
    Column("photo", String(), nullable=True),
    Column("liked_manga", Uuid, nullable=True),
    Column("your_works", Uuid, nullable=True),
    Column("role", Enum(Role, values_callable=lambda obj: [e.value for e in obj]), nullable=True, default=Role.READER),
    Column("date", Date, default=date.today()),
    Column("token", String(), nullable=True),

)



class User:
    pass


db_helper.mapper_registry.map_imperatively(User, user)
