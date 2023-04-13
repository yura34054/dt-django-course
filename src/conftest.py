import uuid

import pytest

from app.internal.models import BankAccount
from app.internal.services import bank_service, user_service


@pytest.fixture
def setup_bank_account(db, django_user_model):
    def make_user_and_bank_account():
        telegram_id = int(uuid.uuid4()) % 10**5
        username = str(uuid.uuid4())
        account_name = str((uuid.uuid4()))

        user_service.create_user(telegram_id, "first_name", username=username)
        bank_service.create_account(telegram_id, account_name)

        BankAccount.objects.filter(owner__telegram_id=telegram_id, name=account_name).update(money=5000)

        return telegram_id, username, account_name

    return make_user_and_bank_account
