from django.http import JsonResponse

from app.internal.services.api_service import get_user_info


def me(request, phone_number):
    return JsonResponse(get_user_info(phone_number))
