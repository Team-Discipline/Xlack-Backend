from fastapi.testclient import TestClient

from app.channel.router import router

client = TestClient(router)


# class ChannelTest(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         pass
#
#     @classmethod
#     def tearDownClass(cls) -> None:
#         pass
#
#     def setUp(self) -> None:
#         pass
#
#     def tearDown(self) -> None:
#         pass


def test_channel_read_by_name(channel_name):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"channel_name": "test_channel_name"}


def test_channel_name_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {"detail": "channel_name not found"}


def test_invalid_keyword_error():
    response = client.get('/')
    assert response.status_code == 400
    assert response.json() == {'detail': "invalid channel name requested"}


def test_db_connection_error():
    response = client.get('/')
    assert response.status_code == 400
    assert response.json() == {'detail': 'db connection error'}


def test_print():
    response = client.get('/')
    assert response.json() == {'print': 'print'}
