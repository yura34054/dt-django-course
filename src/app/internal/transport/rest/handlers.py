import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from app.internal.bot import telegram_bot, update_queue
from app.internal.decorators.api_decorators import requires_auth
from app.internal.services.user_service import get_user_info


@requires_auth
def me(request, phone_number):
    info = get_user_info(phone_number=phone_number)

    if not info or info["phone_number"] == "":
        return JsonResponse({}, status=403)

    return JsonResponse(info, status=200)


@csrf_exempt
def telegram_webhook(request):
    update_queue.put(Update.de_json(json.loads(request.body), telegram_bot))
    return HttpResponse(status=200)
