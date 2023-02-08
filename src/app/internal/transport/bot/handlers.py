import json

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from app.internal.services.telegram_service import handle_update
from config.settings import TELEGRAM_BOT


@csrf_exempt
def telegram_webhook(request: HttpRequest):
    if request.method != "POST":
        return HttpResponseBadRequest()

    if request.META.get("HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN", "") != TELEGRAM_BOT["WEBHOOK_INFO"].get(
        "secret_token", ""
    ):
        return HttpResponseBadRequest()

    update = request.body.decode("utf8")
    handle_update(json.loads(update))

    return HttpResponse(request)
