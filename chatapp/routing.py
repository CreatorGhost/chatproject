from django.urls import re_path

from . import consumers

print("Loading WebSocket URL patterns...")

websocket_urlpatterns = [
    re_path(r'ws/api/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]