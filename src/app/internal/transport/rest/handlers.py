from django.http import JsonResponse

from app.internal.services import api_service


def me(request, phone_number):
    return JsonResponse(api_service(phone_number))
