from sqlalchemy import Column, Table, Uuid,ForeignKey
from app.db import db_helper


liked_manga = Table(
    'liked_manga',
    db_helper.metadata_obj,
    Column("like_id", Uuid, primary_key=True, nullable=False),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("manga_id", Uuid, nullable=False)
)


class Liked:
    pass


db_helper.mapper_registry.map_imperatively(Liked, liked_manga)
