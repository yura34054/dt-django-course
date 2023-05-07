import uuid

import pytest

from app.internal.models import BankAccount, BankCard, User


@pytest.fixture
def setup_user(db, django_user_model):
    def make_user(telegram_id, first_name="first_name", last_name="", username="", phone_number=""):
        user = User.objects.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )

        return user

    return make_user


@pytest.fixture
def setup_friend(db, django_user_model):
    def make_friend(user, friend):
        user.friends.add(friend)

    return make_friend


@pytest.fixture
def setup_bank_account(db, django_user_model):
    def make_bank_account(owner, name, money=5000):
        account = BankAccount.objects.create(
            owner=owner,
            name=name,
            money=money,
        )

        return account

    return make_bank_account


@pytest.fixture
def setup_bank_card(db, django_user_model):
    def make_bank_card(account):
        card = BankCard.objects.create(bank_account=account)

        return card

    return make_bank_card
