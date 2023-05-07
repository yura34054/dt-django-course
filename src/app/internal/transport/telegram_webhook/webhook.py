import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .bot import telegram_bot, update_queue


@csrf_exempt
def telegram_webhook(request):
    update_queue.put(Update.de_json(json.loads(request.body), telegram_bot))
    return HttpResponse(status=200)
