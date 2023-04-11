from django.db import transaction
from django.db.models import Q

from app.internal.models.user import User
from app.internal.models.transaction import Transaction


def create_user(user_info) -> None:
    User.objects.get_or_create(
        telegram_id=user_info.id,
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        username=f"@{user_info.username}",
    )


def update_user_phone(telegram_id, phone_number) -> None:
    user = User.objects.select_for_update().filter(telegram_id=telegram_id)

    user.update(phone_number=phone_number)


def get_user_info(telegram_id=None, phone_number=None) -> dict:
    """return info about user"""

    user = User.objects.filter(Q(telegram_id=telegram_id) | Q(phone_number=phone_number)).get()

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info


def add_friend(telegram_id, friend_username):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id).select_related("friends")
    friend = User.objects.filter(username=friend_username)

    if not friend.exists():
        return f"User {friend_username} not found"

    if user.filter(friends__username=friend_username).exists():
        return f"{friend_username} already in friends"

    friend = friend.get()
    user = user.get()

    user.friends.add(friend)
    user.save(update_fields=("friends",))
    return f"{friend_username} added to friends"


def remove_friend(telegram_id, friend_username):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id).select_related("friends")
    friend = User.objects.filter(username=friend_username)

    if not friend.exists():
        return f"User {friend_username} not found"

    if not user.filter(friends__username=friend_username).exists():
        return f"{friend_username} already not in friends"

    friend = friend.get()
    user = user.get()

    user.friends.remove(friend)
    user.save(update_fields=("friends",))
    return f"{friend_username} removed from friends"


def list_friends(telegram_id):
    user = User.objects.filter(telegram_id=telegram_id).values("friends__username")
    return list(user["friends__username"])


def get_interactions(telegram_id):
    users = User.objects.filter(
        Q(bankaccount__transaction__account_from__owner__telegram_id=telegram_id) &
        Q(bankaccount__transaction__account_to__owner__telegram_id=telegram_id) &
        ~Q(telegram_id)
    ).distinct()

    return users
