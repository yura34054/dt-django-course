from app.internal.models.user import User


def get_user_info(phone_number):
    if not User.objects.filter(phone_number=phone_number).exists():
        return {}

    user = User.objects.get(phone_number=phone_number)

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info
