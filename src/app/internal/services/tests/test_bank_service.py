import pytest

from app.internal.services import bank_service, user_service
from app.internal.models import User, BankAccount, BankCard, Transaction


@pytest.mark.django_db
def test_create_account():
    user_service.create_user(1, 'first_name', username='username')

    assert bank_service.create_account(1, 'account') == 'Account "account" successfully created'
    assert bank_service.create_account(1, 'account') == 'Account "account" already exists'


@pytest.mark.django_db
def test_create_card():
    pass
