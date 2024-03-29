from django.urls import re_path

from notifications import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/notification/$",
        consumers.NotificationsConsumer.as_asgi(),
    ),
]
