import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chatapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')

from channels.routing import ProtocolTypeRouter, URLRouter

import chatapp.routing
from chatproject.middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    ),
})