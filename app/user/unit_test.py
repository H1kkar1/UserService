import unittest
import uuid

from app.user.model import User


class UserTests(unittest.TestCase):
    id = uuid.uuid4()
    user = User(
        id=id,

    )