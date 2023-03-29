from django.db.models import QuerySet, Q

from app.internal.models.bank_account import BankAccount
from app.internal.services.user_service import get_user


def create_account(user_info, name):
    """create new BankAccount object if possible, else return reply message"""

    owner = get_user(user_info.id)

    if get_account(user_info.id, name) is not None:
        return f"Account \"{name}\" already exists"

    BankAccount.objects.create(
        owner=owner,
        name=name,
        money=0,
    )

    return f"Account \"{name}\" successfully created"


def get_account(owner_id, name) -> BankAccount | None:
    """returns BankAccount object if bank account exists, else None"""

    account = BankAccount.objects.filter(Q(owner__telegram_id=owner_id) & Q(name=name))

    if not account.exists():
        return None

    return account.get()


def get_account_info(owner_id, name) -> dict:
    """return info about account if there are any, else empty dict"""

    account = get_account(owner_id, name)

    if account is None:
        return {}

    info = {
        "name": account.name,
        "money": account.money,
        "cards": list((c.name for c in account.bankcard_set.all()))
    }

    return info


def __get_accounts(owner_id) -> QuerySet:
    """returns QuerySet of accounts if there are any, else None"""

    accounts = BankAccount.objects.filter(owner__telegram_id=owner_id)

    return accounts


def get_accounts(owner_id):
    """return info about accounts if there are any, else empty dict"""

    return {a.name: a.money for a in __get_accounts(owner_id)}


def send_money(owner_id, receiver_username, account_name, receiver_account_name, amount):

    amount = round(float(amount), 2)
    account = get_account(owner_id, account_name)

    receiver = get_user(username=receiver_username)
    if receiver is None:
        return f"Receiver {receiver_username} not found"

    if receiver not in get_user(telegram_id=owner_id).friends.all():
        return f"You need to add {receiver_username} to your friend list first by using /add_friend"

    receiver_account = get_account(receiver.telegram_id, receiver_account_name)

    if account is None:
        return f"Account {account_name} not found"

    if receiver_account is None:
        return f"Receiver account {receiver_account_name} not found"

    if account.money < amount:
        return "Not enough money"

    account.money = float(account.money) - amount
    receiver_account.money = float(receiver_account.money) + amount

    account.save()
    receiver_account.save()

    return f"Successfully sent {amount} to {receiver_username}"
