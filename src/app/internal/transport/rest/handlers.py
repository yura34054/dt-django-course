from django.http import JsonResponse

from app.internal.services.user_service import get_user, get_user_info


def me(request, phone_number):
    user = get_user(phone_number=phone_number)
    if user is None:
        return JsonResponse({}, status=403)

    return JsonResponse(get_user_info(user), status=200)
