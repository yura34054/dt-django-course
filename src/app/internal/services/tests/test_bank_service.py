import pytest

from app.internal.exceptions import ValidationError
from app.internal.models import BankAccount, BankCard, Transaction
from app.internal.services import bank_service, user_service


@pytest.mark.django_db
def test_create_account(setup_user):
    setup_user(1, "first_name")
    bank_service.create_account(1, "account")

    assert BankAccount.objects.count() == 1


@pytest.mark.django_db
def test_no_double_account(setup_user):
    setup_user(1, "first_name")
    bank_service.create_account(1, "account")

    with pytest.raises(ValidationError, match='Account "account" already exists'):
        assert bank_service.create_account(1, "account")


@pytest.mark.django_db
def test_multiple_accounts(setup_user):
    setup_user(1, "first_name")
    bank_service.create_account(1, "account")
    bank_service.create_account(1, "account1")

    assert BankAccount.objects.count() == 2


@pytest.mark.django_db
def test_create_card(setup_user, setup_bank_account):
    user = setup_user(1, "first_name")
    setup_bank_account(user, "account")

    bank_service.create_card(1, "account")
    assert BankCard.objects.count() == 1


@pytest.mark.django_db
def test_multiple_cards(setup_user, setup_bank_account):
    user = setup_user(1, "first_name")
    setup_bank_account(user, "account")

    bank_service.create_card(1, "account")
    bank_service.create_card(1, "account")
    assert BankCard.objects.count() == 2


@pytest.mark.django_db
def test_send_money_account(setup_user, setup_bank_account, setup_friend):
    owner_id, username, account_name = 1, "sender", "account"
    receiver_id, receiver_username, receiver_account_name = 2, "receiver", "account"

    setup_bank_account(sender := setup_user(owner_id, username=username), account_name, 5000)
    setup_bank_account(receiver := setup_user(receiver_id, username=receiver_username), account_name, 5000)

    setup_friend(sender, receiver)

    assert (
        bank_service.send_money_account(owner_id, receiver_username, account_name, receiver_account_name, 100.5)
        == 100.5
    )

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4899.5
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.5
    assert Transaction.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "owner_id,receiver_username,account_name,receiver_account_name,amount,error",
    [
        (2, "sender", "receiver_account", "account", 100, "@sender not in friends"),
        (1, "receiver", "account", "receiver_account", -100, "You can't send negative amount of money"),
        (1, "receiver", "other_account", "receiver_account", 100, 'No account "other_account" found'),
        (1, "receiver", "account", "receiver_account", 10000, "Not enough money"),
        (1, "receiver", "account", "other_account", 100, 'No account "other_account" found'),
    ],
)
def test_send_money_account_error(
    owner_id,
    receiver_username,
    account_name,
    receiver_account_name,
    amount,
    error,
    setup_user,
    setup_bank_account,
    setup_friend,
):
    setup_bank_account(sender := setup_user(1, username="sender"), "account", 5000)
    setup_bank_account(receiver := setup_user(2, username="receiver"), "receiver_account", 5000)

    setup_friend(sender, receiver)

    with pytest.raises(ValidationError, match=error):
        bank_service.send_money_account(owner_id, receiver_username, account_name, receiver_account_name, amount)


@pytest.mark.django_db
def test_send_money_card(setup_user, setup_bank_account, setup_friend, setup_bank_card):
    owner_id, account_name = 1, "account"
    receiver_id, receiver_account_name = 2, "receiver_account"

    sender_account = setup_bank_account(sender := setup_user(owner_id, username="sender"), account_name, 5000)
    sender_card_id = setup_bank_card(sender_account).card_id

    receiver_account = setup_bank_account(
        receiver := setup_user(receiver_id, username="receiver"), receiver_account_name, 5000
    )
    receiver_card_id = setup_bank_card(receiver_account).card_id

    setup_friend(sender, receiver)

    assert bank_service.send_money_card(owner_id, sender_card_id, receiver_card_id, 100.5) == 100.5

    assert BankAccount.objects.get(owner__telegram_id=owner_id, name=account_name).money == 4899.5
    assert BankAccount.objects.get(owner__telegram_id=receiver_id, name=receiver_account_name).money == 5100.5
    assert Transaction.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "owner_id,amount,swap_cards,error",
    [
        (1, -100, False, "You can't send negative amount of money"),
        (2, 100, False, 'You don\'t own card "{card_id}"'),
        (1, 10000, False, "Not enough money"),
        (2, 100, True, "@sender not in friends"),
    ],
)
def test_send_money_card_error(
    owner_id, amount, swap_cards, error, setup_user, setup_bank_account, setup_friend, setup_bank_card
):
    sender_account = setup_bank_account(sender := setup_user(1, username="sender"), "account", 5000)
    sender_card = setup_bank_card(sender_account)

    receiver_account = setup_bank_account(receiver := setup_user(2, username="receiver"), "receiver_account", 5000)
    receiver_card = setup_bank_card(receiver_account)

    setup_friend(sender, receiver)

    if swap_cards:
        sender_card, receiver_card = receiver_card, sender_card

    with pytest.raises(ValidationError, match=error.format(card_id=sender_card.card_id)):  # bad but works
        bank_service.send_money_card(owner_id, sender_card.card_id, receiver_card.card_id, amount)
