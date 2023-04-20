from django.urls import path

from app.internal.transport.rest import handlers as rest
from app.internal.transport.rest.auth import LoginAPIView, LogoutAPIView, RefreshAPIView

urlpatterns = [
    path("me/<str:phone_number>", rest.me, name="me"),
    path("telegram-webhook/", rest.telegram_webhook),
    path("login", LoginAPIView.as_view()),
    path("refresh", RefreshAPIView.as_view()),
    path("logout", LogoutAPIView.as_view()),
]
