from rest_framework import authentication, exceptions
from django.conf import settings


class StaticTokenAuthentication(authentication.BaseAuthentication):
    """
    Simple static token authentication.
    Validates Bearer token against STATIC_TOKEN setting.
    Reference: REWRITE_SPECIFICATION.md lines 1089-1148
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise exceptions.AuthenticationFailed('Authorization header missing')

        try:
            token = auth_header.split('Bearer ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid token format')

        # Get expected token from settings
        expected_token = getattr(settings, 'STATIC_TOKEN', 'dev-token-123')

        if token != expected_token:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Return (user, auth) tuple - user can be None for token auth
        return (None, token)
