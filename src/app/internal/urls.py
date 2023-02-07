from django.urls import path

from app.internal.transport.bot import handlers as bot
from app.internal.transport.rest import handlers as rest

urlpatterns = [path("telegram_webhook/", bot.telegram_webhook), path("me/<str:phone_number>", rest.me)]
