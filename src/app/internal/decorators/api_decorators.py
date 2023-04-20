from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from app.internal.authentication import decode_access_token
from app.internal.models import User


def requires_auth(func):
    def wrapper(request, *args, **kwargs):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode("utf-8")
            decode_access_token(token)

            return func(request, *args, **kwargs)

        raise AuthenticationFailed("unauthenticated")

    return wrapper
