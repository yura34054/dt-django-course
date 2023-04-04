import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from app.internal.bot import telegram_bot, update_queue
from app.internal.services.user_service import get_user, get_user_info


def me(request, phone_number):
    user = get_user(phone_number=phone_number)

    if user is None:
        return JsonResponse({}, status=403)

    return JsonResponse(get_user_info(user), status=200)


@csrf_exempt
def telegram_webhook(request):
    update_queue.put(Update.de_json(json.loads(request.body), telegram_bot))
    return HttpResponse(status=200)
