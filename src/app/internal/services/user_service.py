from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

from app.internal.models.user import User


def create_user(telegram_id, first_name, last_name="", username="") -> (User, bool):
    try:
        return User.objects.get(telegram_id=telegram_id), False

    except ObjectDoesNotExist:
        return (
            User.objects.create(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            ),
            True,
        )


def is_phone_set(telegram_id) -> bool:
    user = User.objects.filter(telegram_id=telegram_id).values("phone_number").get()

    return not user["phone_number"] == ""


def update_user_phone(telegram_id, phone_number) -> None:
    user = User.objects.select_for_update().filter(telegram_id=telegram_id)

    user.update(phone_number=phone_number)


def get_user_info(telegram_id=None, phone_number=None) -> dict:
    """return info about user"""

    try:
        user = User.objects.filter(Q(telegram_id=telegram_id) | Q(phone_number=phone_number)).get()
    except ObjectDoesNotExist:
        return {}

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info


def add_friend(telegram_id, friend_username):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id).prefetch_related("friends")
    try:
        friend = User.objects.filter(username=friend_username).get()
    except ObjectDoesNotExist:
        return f"User @{friend_username} not found"

    with transaction.atomic():
        if user.filter(friends__username=friend_username).exists():
            return f"@{friend_username} already in friends"

        user = user.get()
        user.friends.add(friend)
        return f"@{friend_username} added to friends"


def remove_friend(telegram_id, friend_username):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id)
    try:
        friend = User.objects.get(username=friend_username)
    except ObjectDoesNotExist:
        return f"User @{friend_username} not found"

    with transaction.atomic():
        if not user.filter(friends__username=friend_username).exists():
            return f"@{friend_username} already not in friends"

        user = user.get()
        user.friends.remove(friend)
        user.save()
        return f"@{friend_username} removed from friends"


def list_friends(telegram_id):
    friends = User.objects.filter(telegram_id=telegram_id).values("friends__username")
    return list((f["friends__username"] for f in friends))


def get_interactions(telegram_id):
    users = User.objects.filter(
        Q(bankaccount__transaction__account_from__owner__telegram_id=telegram_id)
        & Q(bankaccount__transaction__account_to__owner__telegram_id=telegram_id)
        & ~Q(telegram_id)
    ).distinct()

    return users
