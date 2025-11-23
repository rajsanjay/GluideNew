"""
ASGI config for Gluide consolidated application.

This module configures ASGI to support both HTTP and WebSocket protocols.
WebSocket connections are used for real-time communication with the Gluide AI chatbot.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early to ensure apps are loaded
django_asgi_app = get_asgi_application()

# Import routing and middleware after Django is initialized
from api.routing import websocket_urlpatterns
from api.middleware import AllauthSessionMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AllauthSessionMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
