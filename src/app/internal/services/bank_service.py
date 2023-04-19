from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Q

from app.internal.exceptions import ValidationError
from app.internal.models import BankAccount, BankCard, Transaction, User


def create_account(telegram_id: (str | int), name: str):
    """create new BankAccount object if name isn't taken"""

    owner = User.objects.get(telegram_id=telegram_id)

    account, created = BankAccount.objects.get_or_create(
        owner=owner,
        name=name,
        defaults={"money": 0},
    )

    if not created:
        raise ValidationError(f'Account "{name}" already exists')


def create_card(telegram_id: (str | int), bank_account_name: str) -> int:
    """create new BankCard object, return card's id on success"""

    bank_account = BankAccount.objects.filter(Q(owner__telegram_id=telegram_id) & Q(name=bank_account_name))

    if not bank_account.exists():
        raise ValidationError(f'No account "{bank_account_name}" found')

    card = BankCard.objects.create(
        bank_account=bank_account.get(),
    )

    return card.card_id


def get_account_info(telegram_id: (str | int), name: str) -> dict:
    """return info about account if it exists, else empty dict"""

    try:
        account = BankAccount.objects.filter(Q(owner__telegram_id=telegram_id) & Q(name=name)).get()
    except ObjectDoesNotExist:
        return {}

    info = {
        "name": account.name,
        "money": account.money,
        "cards": list((card["card_id"] for card in account.bankcard_set.values("card_id"))),
    }

    return info


def get_accounts(telegram_id: (str | int)):
    """return info about all accounts associated with user"""

    return {
        account["name"]: account["money"]
        for account in BankAccount.objects.values("name", "money").filter(owner__telegram_id=telegram_id)
    }


def __send_money(account_from: BankAccount, account_to: BankAccount, amount: float):
    account_from.money = F("money") - amount
    account_to.money = F("money") + amount

    account_from.save(update_fields=("money",))
    account_to.save(update_fields=("money",))


def send_money_account(
    owner_id: (str | int),
    receiver_username: str,
    account_name: str,
    receiver_account_name: str,
    amount: (str | int | float),
) -> int:
    """Transfer money from one account to the other if all conditions met, returns amount on success"""

    if not User.objects.filter(telegram_id=owner_id, friends__username=receiver_username).exists():
        raise ValidationError(f"You need to add @{receiver_username} to your friend list first by using /add_friend")

    amount = round(float(amount), 2)
    if amount < 0:
        amount = 0.0

    with transaction.atomic():
        try:
            account_from = (
                BankAccount.objects.select_for_update()
                .filter(Q(owner__telegram_id=owner_id) & Q(name=account_name))
                .get()
            )
        except ObjectDoesNotExist:
            raise ValidationError(f'Account "{account_name}" not found')

        if account_from.money < amount:
            raise ValidationError("Not enough money")

        try:
            account_to = (
                BankAccount.objects.select_for_update()
                .filter(Q(owner__username=receiver_username) & Q(name=receiver_account_name))
                .get()
            )
        except ObjectDoesNotExist:
            raise ValidationError(f'Receiver account "{receiver_account_name}" not found')

        __send_money(account_from, account_to, amount)
        Transaction.objects.create(amount=amount, account_from=account_from, account_to=account_to)
        return amount


def send_money_card(
    owner_id: int, card_id: (str | int), receiver_card_id: (str | int), amount: (str | int | float)
) -> int:
    """Transfer money from one account to the other if all conditions met, return amount on success"""

    amount = round(float(amount), 2)
    if amount < 0:
        amount = 0.0

    with transaction.atomic():
        try:
            card_from = (
                BankCard.objects.select_for_update().filter(card_id=card_id).select_related("bank_account").get()
            )
        except ObjectDoesNotExist:
            raise ValidationError(f'Card "{card_id}" not found')

        if card_from.bank_account.owner.telegram_id != owner_id:
            raise ValidationError(f'You don\'t own card "{card_id}"')

        if card_from.bank_account.money < amount:
            raise ValidationError("Not enough money")

        try:
            card_to = (
                BankCard.objects.select_for_update()
                .filter(card_id=receiver_card_id)
                .select_related("bank_account__owner")
                .get()
            )
        except ObjectDoesNotExist:
            raise ValidationError(f'Receiver card "{receiver_card_id}" not found')

        if not User.objects.filter(telegram_id=owner_id, friends=card_to.bank_account.owner).exists():
            raise ValidationError(
                f'You need to add owner of "{receiver_card_id}" to your friend list first by using /add_friend'
            )

        __send_money(card_from.bank_account, card_to.bank_account, amount)

        Transaction.objects.create(
            amount=amount,
            card_from=card_from,
            account_from=card_from.bank_account,
            card_to=card_to,
            account_to=card_to.bank_account,
        )

    return amount


def get_bank_statement_account(telegram_id: (str | int), account_name: str) -> (dict, int):
    """Get all transactions for account"""

    try:
        account = BankAccount.objects.filter(owner__telegram_id=telegram_id, name=account_name).get()
    except ObjectDoesNotExist:
        raise ValidationError(f"Account {account_name} not found")

    transactions = Transaction.objects.filter(account_from=account).values(
        "account_from__name", "account_to__name", "amount", "time"
    )

    return [
        {
            "time": t["time"].strftime("%d/%m/%Y"),
            "account_from": t["account_from__name"],
            "account_to": t["account_to__name"],
            "amount": round(float(t["amount"]), 2),
        }
        for t in transactions
    ], round(float(account.money), 2)


def get_bank_statement_card(telegram_id: (str | int), card_id: (str | int)) -> (dict, int):
    """Get all transactions for card"""

    try:
        card = (
            BankCard.objects.filter(bank_account__owner__telegram_id=telegram_id, card_id=card_id)
            .select_related("bank_account")
            .get()
        )
    except ObjectDoesNotExist:
        raise ValidationError(f"Card {card_id} not found")

    if card.bank_account.owner.telegram_id != telegram_id:
        raise ValidationError(f"You don't own card {card_id}")

    transactions = Transaction.objects.filter(card_from=card).values(
        "card_from__card_id", "card_to__card_id", "amount", "time"
    )

    return [
        {
            "time": t["time"].strftime("%d/%m/%Y"),
            "card_from": t["card_from__card_id"],
            "card_to": t["card_to__card_id"],
            "amount": round(float(t["amount"]), 2),
        }
        for t in transactions
    ], round(float(card.bank_account.money), 2)
