import unittest
# from fastapi import HTTPException
#
# from app.model.crud.channel import create_channel, read_channel, read_channels, delete_channel, update_channel
# from app.model.database import get_db
from sqlalchemy.orm import Session
# from app.model import models


class ChannelTest(unittest.TestCase):

    def setUpClass(self) -> None:
        self.channel_name: str
        self.db: Session

    def tearDownClass(self) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    # def test_create_channel(self):
    #     channel = create_channel(channel_name="test_channel", db)
