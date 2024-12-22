import unittest
import uuid

from app.db import db_helper
from app.liked_manga.schema import LikeManga
from app.liked_manga.service import like, del_like


class LikedTest(unittest.TestCase):
    def setUp(self):
        self.like_id = uuid.uuid4()
        self.like = LikeManga(id=self.like_id, user_id=self.like_id, manga_id=self.like_id)

    def create_like(self):
        self.assertEqual(
            like(session=db_helper.sessionDep, like=self.like)
        )

    def delete_like(self):
        self.assertEqual(
            del_like(session=db_helper.sessionDep, like_id=self.id)
        )

