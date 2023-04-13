import pytest

from app.internal.services import user_service
from app.internal.models import User


@pytest.mark.django_db
def test_create_user():
    user, created = user_service.create_user(1, 'first_name', 'last_name', 'username')
    assert User.objects.count() == 1
    assert created
    assert user.telegram_id == 1
    assert user.first_name == 'first_name'
    assert user.last_name == 'last_name'
    assert user.username == 'username'

    user_service.create_user(1, 'first_name')
    assert User.objects.count() == 1

    user_service.create_user(2, 'first_name')
    assert User.objects.count() == 2


@pytest.mark.django_db
def test_user_phone():
    user_service.create_user(1, 'first_name')
    assert not user_service.is_phone_set(1)

    user_service.update_user_phone(1, '71234567890')
    assert user_service.is_phone_set(1)
    assert User.objects.get(telegram_id=1).phone_number == '71234567890'


@pytest.mark.django_db
def test_get_user_info():
    user_service.create_user(1, 'first_name', 'last_name', 'username')
    user_service.update_user_phone(1, '71234567890')
    assert user_service.get_user_info(telegram_id=1) == {
        "first_name": 'first_name',
        "last_name": 'last_name',
        "username": 'username',
        "phone_number": '71234567890',
    }


@pytest.mark.django_db
def test_user_friends():
    user_service.create_user(1, 'first_name', username='username_1')

    assert user_service.add_friend(1, 'username_2') == "User @username_2 not found"
    assert user_service.remove_friend(1, 'username_2') == "User @username_2 not found"
    assert user_service.list_friends(1) == [None]

    user_service.create_user(2, 'first_name', username='username_2')

    assert user_service.remove_friend(1, 'username_2') == "@username_2 already not in friends"
    assert user_service.add_friend(1, 'username_2') == "@username_2 added to friends"
    assert user_service.add_friend(1, 'username_2') == "@username_2 already in friends"
    assert user_service.list_friends(1) == ['username_2']

    assert user_service.remove_friend(1, 'username_2') == "@username_2 removed from friends"
    assert user_service.list_friends(1) == [None]
    assert user_service.remove_friend(1, 'username_2') == "@username_2 already not in friends"


@pytest.mark.django_db
def test_user_get_interactions():
    pass
