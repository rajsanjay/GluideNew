"""
WebSocket URL routing for the API application.

This module defines WebSocket URL patterns for real-time features:
- Real-time chat between counselor and student
- AI guidance with streaming responses

CRITICAL: These URL patterns are used by the frontend WebSocket client.
DO NOT modify the patterns without updating the frontend client.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Real-time chat between counselor and student
    # Example: ws://localhost:8000/ws/chat/room123/
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),

    # AI guidance with streaming responses
    # Example: ws://localhost:8000/ws/ask-gluide/session_abc123/
    re_path(r"ws/ask-gluide/(?P<room_name>[^/]+)/$", consumers.GluideAiWithStreaming.as_asgi()),
]
