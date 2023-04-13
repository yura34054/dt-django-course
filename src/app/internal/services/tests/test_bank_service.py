import pytest

from app.internal.services import bank_service, user_service
from app.internal.models import BankAccount, BankCard, Transaction


@pytest.mark.django_db
def test_create_account():
    user_service.create_user(1, 'first_name')

    assert bank_service.create_account(1, 'account') == 'Account "account" successfully created'
    assert BankAccount.objects.count() == 1
    assert bank_service.create_account(1, 'account') == 'Account "account" already exists'
    assert BankAccount.objects.count() == 1


@pytest.mark.django_db
def test_create_card(setup_bank_account):
    telegram_id, username, account_name = setup_bank_account()

    assert bank_service.create_card(telegram_id, 'abc') == 'No account "abc" found'
    card_id, message = bank_service.create_card(telegram_id, account_name)
    assert message == f'Card "{card_id}" successfully created'
    assert BankCard.objects.count() == 1

    card_id, message = bank_service.create_card(telegram_id, account_name)
    assert message == f'Card "{card_id}" successfully created'
    assert BankCard.objects.count() == 2


@pytest.mark.django_db
def test_send_money_account(setup_bank_account):
    # this one maybe can be improved with @pytest.mark.parametrize, but I'm too dumb for to know how
    owner_id, username, account_name = setup_bank_account()
    receiver_id, receiver_username, receiver_account_name = setup_bank_account()

    assert bank_service.send_money_account(
        owner_id, 
        receiver_username, 
        account_name, 
        receiver_account_name, 
        100
    ) == f"You need to add @{receiver_username} to your friend list first by using /add_friend"

    user_service.add_friend(owner_id, receiver_username)

    assert bank_service.send_money_account(
        owner_id, 
        receiver_username, 
        'abc', 
        receiver_account_name, 
        100
    ) == f"Account \"abc\" not found"

    assert bank_service.send_money_account(
        owner_id, 
        receiver_username, 
        account_name, 
        receiver_account_name, 
        100000
    ) == "Not enough money"

    assert bank_service.send_money_account(
        owner_id, 
        receiver_username, 
        account_name, 
        'abc',
        100
    ) == f"Receiver account \"abc\" not found"

    assert bank_service.send_money_account(
        owner_id,
        receiver_username,
        account_name,
        receiver_account_name,
        100
    ) == f"Successfully sent 100.0 to @{receiver_username}"

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 1

    assert bank_service.send_money_account(
        owner_id,
        receiver_username,
        account_name,
        receiver_account_name,
        -100
    ) == f"Successfully sent 0.0 to @{receiver_username}"

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 2


@pytest.mark.django_db
def test_send_money_card(setup_bank_account):
    assert BankCard.objects.count() == 0
    assert BankAccount.objects.count() == 0

    owner_id, username, account_name = setup_bank_account()
    receiver_id, receiver_username, receiver_account_name = setup_bank_account()

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=0,
        receiver_card_id=0,
        amount=100
    ) == "Card \"0\" not found"

    sender_card_id = bank_service.create_card(owner_id, account_name)[0]
    receiver_card_id = bank_service.create_card(receiver_id, receiver_account_name)[0]

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=receiver_card_id,
        receiver_card_id=sender_card_id,
        amount=100
    ) == f"You don't own card \"{receiver_card_id}\""

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=sender_card_id,
        receiver_card_id=0,
        amount=100
    ) == "Receiver card \"0\" not found"

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=sender_card_id,
        receiver_card_id=receiver_card_id,
        amount=100
    ) == f"You need to add owner of \"{receiver_card_id}\" to your friend list first by using /add_friend"

    user_service.add_friend(owner_id, receiver_username)

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=sender_card_id,
        receiver_card_id=receiver_card_id,
        amount=100
    ) == f"Successfully sent 100.0 to card \"{receiver_card_id}\""

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 1

    assert bank_service.send_money_card(
        owner_id=owner_id,
        card_id=sender_card_id,
        receiver_card_id=receiver_card_id,
        amount=-100
    ) == f"Successfully sent 0.0 to card \"{receiver_card_id}\""

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4900.0
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.0
    assert Transaction.objects.count() == 2
