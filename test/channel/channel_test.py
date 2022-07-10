import unittest

from sqlalchemy import create_engine

from app.channel.router import channel_create

# from app.model import models

engine = create_engine(url="app.model.database")


class ChannelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_channel(self):
        my_db = {
            'channel': 'test_channel_name'
        }
        channel_test = channel_create(channel_name="test_channel_name", db=my_db)
