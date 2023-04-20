from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from app.internal.authentication import create_access_token, create_refresh_token, decode_refresh_token
from app.internal.models import User


class LoginAPIView(APIView):
    def post(self, request):
        try:
            user = User.objects.filter(username=request.data["username"], logged_in=True).get()

        except ObjectDoesNotExist:
            raise APIException("Invalid credentials!")

        access_token = create_access_token(user.telegram_id)
        refresh_token = create_refresh_token(user.telegram_id)

        response = Response()

        response.set_cookie(key="refreshToken", value=refresh_token, httponly=True)
        response.data = {"token": access_token}

        return response


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refreshToken")
        telegram_id = decode_refresh_token(refresh_token)
        access_token = create_access_token(telegram_id)
        return Response({"token": access_token})


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {"message": "success"}
        return response
