from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from prometheus_client import Counter

from app.internal.exceptions import AlreadyInFriendsError, NotInFriendsError, UserNotFoundError
from app.internal.models import User

friends_counter = Counter("friends_counter", "number of friends made")


def create_user(telegram_id: (int, str), first_name: str, last_name="", username="") -> (User, bool):
    """Create new user if id isn't taken, return User object and whether it was created"""

    user = User.objects.filter(telegram_id=telegram_id).first()
    if user is not None:
        return user, False

    return (
        User.objects.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        ),
        True,
    )


def update_user(telegram_id: (int, str), first_name: str, last_name="", username="", phone_number=""):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id)
    user.update(first_name=first_name, last_name=last_name, username=username, phone_number=phone_number)


def is_phone_set(telegram_id: (int, str)) -> bool:
    """Check if user's phone is set"""

    user = User.objects.filter(telegram_id=telegram_id).values("phone_number").get()
    return not user["phone_number"] == ""


def update_user_phone(telegram_id: (int, str), phone_number: (int, str)) -> None:
    """Update user's phone"""

    user = User.objects.select_for_update().filter(telegram_id=telegram_id)
    user.update(phone_number=phone_number)


def get_user_info(telegram_id: (int, str) = None, phone_number: (int, str) = None) -> dict:
    """Return info about user"""

    user = User.objects.filter(Q(telegram_id=telegram_id) | Q(phone_number=phone_number)).first()

    if user is None:
        return {}

    user_info = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone_number": user.phone_number,
    }

    return user_info


def add_friend(telegram_id: (int, str), friend_username: str) -> None:
    """Add new friend to user's friends"""

    user = User.objects.select_for_update().filter(telegram_id=telegram_id).prefetch_related("friends")
    friend = User.objects.filter(username=friend_username).first()
    if friend is None:
        raise UserNotFoundError(friend_username)

    with transaction.atomic():
        if user.filter(friends__username=friend_username).exists():
            raise AlreadyInFriendsError(friend_username)

        user = user.get()
        user.friends.add(friend)

    friends_counter.inc()


def remove_friend(telegram_id: (int, str), friend_username: str) -> None:
    """Remove existing friend from user's friends"""

    user = User.objects.select_for_update().filter(telegram_id=telegram_id)

    friend = User.objects.filter(username=friend_username).first()
    if friend is None:
        raise UserNotFoundError(friend_username)

    with transaction.atomic():
        if not user.filter(friends__username=friend_username).exists():
            raise NotInFriendsError(friend_username)

        user = user.get()
        user.friends.remove(friend)
        user.save()


def list_friends(telegram_id: (int, str)) -> list:
    """Return list of user's friends names"""

    friends = User.objects.filter(telegram_id=telegram_id).values("friends__username")
    friends = list((f["friends__username"] for f in friends))
    return [] if friends == [None] else friends


def get_interactions(telegram_id: (int, str)):
    """Return all users with whom user interacted"""

    users = (
        User.objects.filter(
            Q(bankaccount__account_from__account_to__owner_id=telegram_id)
            | Q(bankaccount__account_from__account_from__owner_id=telegram_id)
            | Q(bankaccount__account_to__account_to__owner_id=telegram_id)
            | Q(bankaccount__account_to__account_from__owner_id=telegram_id),
            ~Q(telegram_id=telegram_id),
        )
        .distinct()
        .values("username")
    )

    return list((u["username"] for u in users))


def set_password(telegram_id: int, password: str):
    user = User.objects.select_for_update().filter(telegram_id=telegram_id)
    user.update(password=make_password(password))
