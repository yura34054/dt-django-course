import pytest

from app.internal.models import User
from app.internal.services import user_service


@pytest.mark.django_db
def test_create_user():
    user, created = user_service.create_user(1, "first_name", "last_name", "username")

    assert User.objects.count() == 1
    assert created
    assert user.telegram_id == 1
    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert user.username == "username"
    assert not user_service.is_phone_set(1)
    assert user_service.list_friends(1) == []


@pytest.mark.django_db
def test_no_double_user():
    user_service.create_user(1, "first_name", "last_name", "username")
    user_service.create_user(1, "other_first_name")

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_multiple_users():
    user_service.create_user(1, "first_name")
    user_service.create_user(2, "first_name")

    assert User.objects.count() == 2


@pytest.mark.django_db
def test_user_phone(setup_user):
    setup_user(1, "first_name")

    user_service.update_user_phone(1, "71234567890")

    assert user_service.is_phone_set(1)
    assert User.objects.get(telegram_id=1).phone_number == "71234567890"


@pytest.mark.django_db
def test_get_user_info(setup_user):
    setup_user(1, "first_name", "last_name", "username", "71234567890")

    assert user_service.get_user_info(telegram_id=1) == {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "phone_number": "71234567890",
    }


@pytest.mark.django_db
def test_user_add_friends(setup_user):
    setup_user(1, "first_name", username="username_1")
    setup_user(2, "first_name", username="username_2")

    user_service.add_friend(1, "username_2")
    assert user_service.list_friends(1) == ["username_2"]


@pytest.mark.django_db
def test_user_remove_friends(setup_user):
    setup_user(1, "first_name", username="username_1")
    setup_user(2, "first_name", username="username_2")
    user_service.add_friend(1, "username_2")

    user_service.remove_friend(1, "username_2")
    assert user_service.list_friends(1) == []
