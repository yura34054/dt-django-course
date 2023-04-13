from django.db.models import Q

from app.internal.models.user import User


def create_user(user_info) -> None:
    if get_user(telegram_id=user_info.id) is not None:
        return

    User.objects.create(
        telegram_id=user_info.id,
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        username=f"@{user_info.username}",
    )


def get_user(telegram_id=None, phone_number=None, username=None) -> User | None:
    """returns User object if user exists, else None"""

    user = User.objects.filter(Q(telegram_id=telegram_id) | Q(phone_number=phone_number) | Q(username=username))
    if not user.exists():
        return None

    return user.get()


def update_user_phone(user: User, phone_number) -> None:
    user.phone_number = phone_number
    user.save()


def get_user_info(user: User) -> dict:
    """return info about user if he has his phone set, else empty dict"""

    if user.phone_number == "":
        return {}

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info


def add_friend(user_id, friend_username):
    user = get_user(telegram_id=user_id)
    friend = get_user(username=friend_username)

    if friend is None:
        return f"User {friend_username} not found"

    if friend in user.friends.all():
        return f"{friend_username} already in friends"

    user.friends.add(friend)
    user.save()
    return f"{friend_username} added to friends"


def remove_friend(user_id, friend_username):
    user = get_user(telegram_id=user_id)
    friend = get_user(username=friend_username)

    if friend is None:
        return f"User {friend_username} not found"

    if friend not in user.friends.all():
        return f"{friend_username} already not in friends"

    user.friends.remove(friend)
    user.save()
    return f"{friend_username} removed from friends"


def list_friends(user_id):
    return list((f.username for f in get_user(telegram_id=user_id).friends.all()))
