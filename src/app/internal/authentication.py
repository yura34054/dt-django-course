import datetime

import jwt
from jwt.exceptions import PyJWTError
from ninja.security import HttpBearer

from app.internal.exceptions.validation_errors import UnauthorizedRequest


def create_access_token(telegram_id):
    return jwt.encode(
        {
            "telegram_id": telegram_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "iat": datetime.datetime.utcnow(),
        },
        "access_secret",
        algorithm="HS256",
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, "access_secret", algorithms="HS256")

        return payload["telegram_id"]

    except PyJWTError:
        raise UnauthorizedRequest


def create_refresh_token(telegram_id):
    return jwt.encode(
        {
            "telegram_id": telegram_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=15),
            "iat": datetime.datetime.utcnow(),
        },
        "refresh_secret",
        algorithm="HS256",
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms="HS256")

        return payload["telegram_id"]

    except PyJWTError:
        raise UnauthorizedRequest


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        return decode_access_token(token)
