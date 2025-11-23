"""
Custom middleware for Django Channels WebSocket authentication.

This module provides middleware for WebSocket connections,
extracting session_id from query parameters and authenticating users.

Authentication flow:
    Frontend passes session_id as query parameter:
    ws://host/ws/chat/123/?session_id=abc123

    Middleware:
    1. Extracts session_id from query string
    2. Validates session against Django's session store
    3. Attaches user to WebSocket scope
    4. Passes authenticated scope to consumer
"""

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()


class AllauthSessionMiddleware(BaseMiddleware):
    """
    Custom middleware for WebSocket authentication via session ID.

    This middleware extracts the session_id from the WebSocket connection's
    query string, validates it against Django's session store, and attaches
    the authenticated user to the scope.

    Usage in ASGI configuration:
        AllauthSessionMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )

    WebSocket connection example:
        ws://localhost:8000/ws/chat/room123/?session_id=abc123def456
    """

    async def __call__(self, scope, receive, send):
        """
        Process the WebSocket connection and authenticate the user.

        Args:
            scope: ASGI connection scope
            receive: ASGI receive callable
            send: ASGI send callable

        Returns:
            Processed scope with authenticated user attached
        """
        # Extract session_id from query string
        query_string = scope.get('query_string', b'').decode()

        # Parse query parameters
        params = dict(
            param.split('=')
            for param in query_string.split('&')
            if '=' in param
        )

        session_id = params.get('session_id')

        # Authenticate user from session_id
        if session_id:
            scope['user'] = await self.get_user_from_session(session_id)
        else:
            scope['user'] = None

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_session(self, session_id):
        """
        Retrieve user from Django session.

        Args:
            session_id: Django session key

        Returns:
            User object if session is valid and user exists, None otherwise
        """
        try:
            # Get session from database
            session = Session.objects.get(session_key=session_id)

            # Decode session data and extract user ID
            user_id = session.get_decoded().get('_auth_user_id')

            # Return user object
            return User.objects.get(id=user_id)

        except (Session.DoesNotExist, User.DoesNotExist, KeyError, TypeError):
            # Session doesn't exist, user doesn't exist, or session data is invalid
            return None


def AllauthSessionMiddlewareStack(inner):
    """
    Factory function to wrap the inner application with authentication middleware.

    Args:
        inner: The inner ASGI application (typically URLRouter)

    Returns:
        AllauthSessionMiddleware instance wrapping the inner application
    """
    return AllauthSessionMiddleware(inner)
