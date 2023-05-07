from django.urls import path

from app.internal.transport.rest.api import get_api
from app.internal.transport.telegram_webhook.webhook import telegram_webhook

urlpatterns = [
    path("telegram-webhook/", telegram_webhook),
    path("", get_api().urls),
]
