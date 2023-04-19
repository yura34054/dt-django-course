import pytest

from app.internal.exceptions import ValidationError
from app.internal.models import BankAccount, BankCard, Transaction
from app.internal.services import bank_service, user_service


@pytest.mark.django_db
def test_create_account():
    user_service.create_user(1, "first_name")

    bank_service.create_account(1, "account")
    assert BankAccount.objects.count() == 1

    try:
        assert bank_service.create_account(1, "account")
        raise Exception

    except ValidationError as e:
        assert str(e) == 'Account "account" already exists'
        assert BankAccount.objects.count() == 1


@pytest.mark.django_db
def test_create_card(setup_bank_account):
    telegram_id, username, account_name = setup_bank_account()

    try:
        bank_service.create_card(telegram_id, "abc")
        raise Exception
    except ValidationError as e:
        assert str(e) == 'No account "abc" found'

    bank_service.create_card(telegram_id, account_name)
    assert BankCard.objects.count() == 1

    bank_service.create_card(telegram_id, account_name)
    assert BankCard.objects.count() == 2


@pytest.mark.django_db
def test_send_money_account(setup_bank_account):
    # this one maybe can be improved with @pytest.mark.parametrize, but I'm too dumb for to know how
    owner_id, username, account_name = setup_bank_account()
    receiver_id, receiver_username, receiver_account_name = setup_bank_account()
    user_service.add_friend(owner_id, receiver_username)

    try:
        bank_service.send_money_account(owner_id, receiver_username, account_name, receiver_account_name, 100000)
        raise Exception

    except ValidationError as e:
        assert str(e) == "Not enough money"

    assert (
        bank_service.send_money_account(owner_id, receiver_username, account_name, receiver_account_name, 100) == 100.0
    )

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 1

    assert (
        bank_service.send_money_account(owner_id, receiver_username, account_name, receiver_account_name, -100) == 0.0
    )

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 2


@pytest.mark.django_db
def test_send_money_card(setup_bank_account):
    assert BankCard.objects.count() == 0
    assert BankAccount.objects.count() == 0

    owner_id, username, account_name = setup_bank_account()
    receiver_id, receiver_username, receiver_account_name = setup_bank_account()
    user_service.add_friend(owner_id, receiver_username)

    sender_card_id = bank_service.create_card(owner_id, account_name)
    receiver_card_id = bank_service.create_card(receiver_id, receiver_account_name)

    try:
        bank_service.send_money_card(owner_id, receiver_card_id, sender_card_id, 100)
        raise Exception

    except ValidationError as e:
        assert str(e) == f'You don\'t own card "{receiver_card_id}"'

    try:
        bank_service.send_money_card(owner_id, sender_card_id, receiver_card_id, 100000)
        raise Exception

    except ValidationError as e:
        assert str(e) == "Not enough money"

    assert bank_service.send_money_card(owner_id, sender_card_id, receiver_card_id, 100) == 100.0

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 1

    assert bank_service.send_money_card(owner_id, sender_card_id, receiver_card_id, -100) == 0.0

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 2
