from django.db import transaction
from django.db.models import F, Q

from app.internal.models.bank_account import BankAccount
from app.internal.models.bank_card import BankCard
from app.internal.models.transaction import Transaction
from app.internal.models.user import User


def create_account(user_id, name):
    """create new BankAccount object if name isn't taken, else return reply message"""

    owner = User.objects.get(telegram_id=user_id)

    account, created = BankAccount.objects.get_or_create(owner=owner, name=name)
    if not created:
        return f'Account "{name}" already exists'

    return f'Account "{name}" successfully created'


def create_card(user_info, bank_account_name):
    """create new BankCard object"""

    bank_account = BankAccount.objects.filter(Q(owner__telegram_id=user_info.id) & Q(name=bank_account_name))

    if not bank_account.exists():
        return f'No account "{bank_account_name}" found'

    card = BankCard.objects.create(
        bank_account=bank_account.get(),
    )

    return f'Card "{card.card_id}" successfully created'


def get_account_info(owner_id, name) -> dict:
    """return info about account if it exists, else empty dict"""

    account = BankAccount.objects.filter(Q(owner__telegram_id=owner_id) & Q(name=name))

    if not account.exists():
        return {}

    info = {
        "name": account.name,
        "money": account.money,
        "cards": list((card["id"] for card in account.bankcard_set.values("name"))),
    }

    return info


def get_accounts(owner_id):
    """return info about all accounts associated with user"""

    return {
        account["name"]: account["money"]
        for account in BankAccount.objects.values("name", "money").filter(owner__telegram_id=owner_id)
    }


def send_money(account_from, account_to, amount):
    account_from = F("money") - amount
    account_to = F("money") + amount

    account_from.save(update_fields=("money",))
    account_to.save(update_fields=("money",))


def send_money_account(owner_id, receiver_username, account_name, receiver_account_name, amount):
    if User.objects.filter(Q(telegram_id=owner_id) & Q(friends__username=receiver_username)).exists:
        return f"You need to add {receiver_username} to your friend list first by using /add_friend"

    amount = round(float(amount), 2)
    if amount < 0:
        amount = 0

    account_from = BankAccount.objects.select_for_update().filter(Q(owner__telegram_id=owner_id) & Q(name=account_name))

    if not account_from.exists():
        return f"Account {account_name} not found"

    account_to = BankAccount.objects.select_for_update().filter(
        Q(owner__username=receiver_username) & Q(name=receiver_account_name)
    )

    if not account_to.exists():
        return f"Receiver account {receiver_account_name} not found"

    with transaction.atomic():
        account_from = account_from.get()
        account_to = account_to.get()

        if account_from.money < amount:
            return "Not enough money"

        send_money(account_from, account_to, amount)

        Transaction.objects.create(amount=amount, account_from=account_from, account_to=account_to)

    return f"Successfully sent {amount} to {receiver_username}"


def send_money_card(owner_id, card_id, receiver_card_id, amount):
    amount = round(float(amount), 2)
    if amount < 0:
        amount = 0

    card_from = BankCard.objects.select_for_update()\
        .filter(card_id=card_id).select_related("bank_account__owner__telegram_id")

    if not card_from.exists():
        return f"Card {receiver_card_id} not found"

    card_to = BankCard.objects.select_for_update()\
        .filter(card_id=receiver_card_id).select_related("bank_account__owner")

    if not card_to.exists():
        return f"Receiver card {receiver_card_id} not found"

    with transaction.atomic():
        card_from = card_from.get()

        if card_from.bank_account.owner.telegram_id != owner_id:
            return f"You don't own {card_id}"

        card_to = card_to.get()

        if User.objects.filter(Q(telegram_id=owner_id) & Q(friends=card_to.bank_account.owner)).exists:
            return f"You need to add owner of {receiver_card_id} to your friend list first by using /add_friend"

        send_money(card_from.bank_account, card_to.bank_account, amount)

        Transaction.objects.create(
            amount=amount,
            card_from=card_from,
            account_from=card_from.bank_account,
            card_to=card_to,
            account_to=card_to.bank_account,
        )

    return f"Successfully sent {amount} to {receiver_card_id}"


def get_bank_statement_account(telegram_id, account_name):
    account = BankAccount.objects\
        .filter(Q(owner__telegram_id=telegram_id) & Q(name=account_name))

    if not account.exists():
        return f"Account {account_name} not found"

    transactions = Transaction.objects\
        .filter(account_from=account)[100:]

    if not transactions.exists():
        return f"No transactions for account {account_name} found"

    return transactions.all(), account.money


def get_bank_statement_card(telegram_id, card_id):
    card = BankAccount.objects\
        .filter(Q(bank_account__owner__telegram_id=telegram_id) & Q(card_id=card_id))\
        .select_related("bank_account__owner", "bank_account__money")

    if not card.exists():
        return f"Card {card_id} not found"

    card.get()

    if card.bank_account.owner.telegram_id != telegram_id:
        return f"You don't own {card_id}"

    transactions = Transaction.objects.filter(card_from=card)[100:]

    if not transactions.exists():
        return f"No transactions for card {card_id} found"

    return transactions.all()
