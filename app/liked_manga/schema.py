from pydantic import BaseModel, UUID4


class LikeManga(BaseModel):
    like_id: UUID4
    user_id: UUID4
    manga_id: UUID4