from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from app.internal.authentication import create_access_token, create_refresh_token, decode_refresh_token
from app.internal.exceptions.validation_errors import UnauthorizedRequest
from app.internal.models import User
from app.internal.transport.rest.users.schemas import UserIn


def login(request, user_in: UserIn, response: HttpResponse):
    user = User.objects.filter(username=user_in.username).first()

    if user is None:
        raise UnauthorizedRequest

    if not check_password(user_in.password, user.password):
        raise UnauthorizedRequest

    access_token = create_access_token(user.telegram_id)
    refresh_token = create_refresh_token(user.telegram_id)

    response.set_cookie(key="refreshToken", value=refresh_token, httponly=True)
    return {"token": access_token}


def refresh(request):
    refresh_token = request.COOKIES.get("refreshToken")
    telegram_id = decode_refresh_token(refresh_token)
    access_token = create_access_token(telegram_id)
    return {"token": access_token}


def logout(request, response: HttpResponse):
    response.delete_cookie(key="refreshToken")
    return {"message": "logged out"}
