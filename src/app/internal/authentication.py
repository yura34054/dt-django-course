import datetime

import jwt
from rest_framework import exceptions


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
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")


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
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")
