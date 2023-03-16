from django.http import JsonResponse

from app.internal.services.user_service import get_user, get_user_info


def me(request, phone_number):
    user = get_user(phone_number=phone_number)
    user_info = get_user_info(user)

    return JsonResponse(user_info, status=403 if len(user_info) == 0 else 200)
