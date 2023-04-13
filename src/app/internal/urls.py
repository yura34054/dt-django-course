from django.urls import path

from app.internal.transport.rest import handlers as rest

urlpatterns = [path("me/<str:phone_number>", rest.me, name="me"), path("telegram-webhook/", rest.telegram_webhook)]
