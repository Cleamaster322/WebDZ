from django.urls import re_path

from .consumers import ProtocolConsumer

websocket_urlpatterns = [
    re_path(r"ws/protocols/$", ProtocolConsumer.as_asgi()),
]