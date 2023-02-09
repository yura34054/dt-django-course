from django.db.models import Q, QuerySet

from app.internal.models.user import User


def create_user(user_info) -> User:
    if get_user(chat_id=user_info["id"]) is not None:
        return

    User.objects.create(
        chat_id=user_info["id"],
        first_name=user_info["first_name"],
        last_name=user_info.get("last_name", ""),
        username=user_info.get("username", ""),
    )


def get_user(chat_id=None, phone_number=None) -> QuerySet | None:
    """returns QuerySet object if user exists, else None"""

    user = User.objects.filter(Q(chat_id=chat_id) | Q(phone_number=phone_number))
    if not user.exists():
        return None

    return user


def update_user_phone(user: QuerySet, phone_number) -> None:
    user.update(phone_number=phone_number)


def get_user_info(user: User) -> dict:
    """return info about user if he has his phone set, else empty dict"""
    if user.phone_number is None:
        return None

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info
