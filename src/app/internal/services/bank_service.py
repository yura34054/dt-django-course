import io

from django.core.files.images import ImageFile
from django.db import transaction
from django.db.models import F, Q

from app.internal.exceptions import (
    AccountAlreadyExistsError,
    AccountNotFoundError,
    CardNotFoundError,
    CardPermissionError,
    NegativeMoneyAmountError,
    NotEnoughMoneyError,
    NotInFriendsError,
)
from app.internal.models import BankAccount, BankCard, Transaction, User
from app.internal.storage.yandex_s3 import get_presigned_link


def create_account(telegram_id: (str | int), name: str):
    """create new BankAccount object if name isn't taken"""

    owner = User.objects.get(telegram_id=telegram_id)

    account, created = BankAccount.objects.get_or_create(
        owner=owner,
        name=name,
        defaults={"money": 0},
    )

    if not created:
        raise AccountAlreadyExistsError(name)


def create_card(telegram_id: (str | int), bank_account_name: str) -> int:
    """create new BankCard object, return card's id on success"""

    bank_account = BankAccount.objects.filter(Q(owner__telegram_id=telegram_id) & Q(name=bank_account_name)).first()

    if bank_account is None:
        raise AccountNotFoundError(bank_account_name)

    card = BankCard.objects.create(
        bank_account=bank_account.get(),
    )

    return card.card_id


def get_account_info(telegram_id: (str | int), name: str) -> dict:
    """return info about account if it exists, else empty dict"""

    account = BankAccount.objects.filter(Q(owner__telegram_id=telegram_id) & Q(name=name)).first()
    if account is None:
        return {}

    info = {
        "name": account.name,
        "money": account.money,
        "cards": list((card["card_id"] for card in account.bankcard_set.values("card_id"))),
    }

    return info


def get_accounts(telegram_id: (str | int)):
    """return info about all accounts associated with user"""

    return [
        {"name": account.name, "money": account.money, "cards": (c.card_id for c in account.bankcard_set.all())}
        for account in BankAccount.objects.filter(owner__telegram_id=telegram_id).prefetch_related("bankcard_set")
    ]


def __send_money(amount, account_from, account_to, card_from=None, card_to=None, postcard=None):
    account_from.money = F("money") - amount
    account_to.money = F("money") + amount

    account_from.save(update_fields=("money",))
    account_to.save(update_fields=("money",))

    Transaction.objects.create(
        amount=amount,
        account_from=account_from,
        card_from=card_from,
        account_to=account_to,
        card_to=card_to,
        has_postcard=postcard is not None,
        postcard=ImageFile(
            io.BytesIO(bytes(postcard.get_file().download_as_bytearray())), name=postcard.file_unique_id + ".png"
        ),
    )


def send_money_account(
    owner_id: (str | int),
    receiver_username: str,
    account_name: str,
    receiver_account_name: str,
    amount: (str | int | float),
    postcard=None,
) -> float:
    """Transfer money from one account to the other if all conditions met, returns amount on success"""

    amount = round(float(amount), 2)
    if amount < 0:
        raise NegativeMoneyAmountError

    if not User.objects.filter(telegram_id=owner_id, friends__username=receiver_username).exists():
        raise NotInFriendsError(receiver_username)

    with transaction.atomic():
        account_from = (
            BankAccount.objects.select_for_update()
            .filter(Q(owner__telegram_id=owner_id) & Q(name=account_name))
            .first()
        )
        if account_from is None:
            raise AccountNotFoundError(account_name)

        if account_from.money < amount:
            raise NotEnoughMoneyError

        account_to = (
            BankAccount.objects.select_for_update()
            .filter(Q(owner__username=receiver_username) & Q(name=receiver_account_name))
            .first()
        )
        if account_to is None:
            raise AccountNotFoundError(receiver_account_name)

        __send_money(amount=amount, account_from=account_from, account_to=account_to, postcard=postcard)

        return amount


def send_money_card(
    owner_id: int, card_id: (str | int), receiver_card_id: (str | int), amount: (str | int | float), postcard=None
) -> float:
    """Transfer money from one account to the other if all conditions met, return amount on success"""

    amount = round(float(amount), 2)
    if amount < 0:
        raise NegativeMoneyAmountError

    with transaction.atomic():
        card_from = BankCard.objects.select_for_update().filter(card_id=card_id).select_related("bank_account").first()
        if card_from is None:
            raise CardNotFoundError(card_id)

        if card_from.bank_account.owner.telegram_id != owner_id:
            raise CardPermissionError(card_id)

        if card_from.bank_account.money < amount:
            raise NotEnoughMoneyError

        card_to = (
            BankCard.objects.select_for_update()
            .filter(card_id=receiver_card_id)
            .select_related("bank_account__owner")
            .first()
        )
        if card_to is None:
            raise CardNotFoundError(receiver_card_id)

        if not User.objects.filter(telegram_id=owner_id, friends=card_to.bank_account.owner).exists():
            raise NotInFriendsError(card_to.bank_account.owner.username)

        __send_money(
            amount=amount,
            card_from=card_from,
            account_from=card_from.bank_account,
            card_to=card_to,
            account_to=card_to.bank_account,
            postcard=postcard,
        )

    return amount


def get_bank_statement_account(telegram_id: (str | int), account_name: str) -> (dict, int):
    """Get all transactions for account"""

    account = BankAccount.objects.filter(owner__telegram_id=telegram_id, name=account_name).first()
    if account is None:
        raise AccountNotFoundError(account_name)

    transactions = Transaction.objects.filter(Q(account_from=account) | Q(account_to=account)).distinct()

    bank_statement = __compile_account_transactions(transactions)
    transactions.update(read=True)

    return bank_statement, round(float(account.money), 2)


def get_bank_statement_card(telegram_id: (str | int), card_id: (str | int)) -> (dict, int):
    """Get all transactions for card"""

    card = (
        BankCard.objects.filter(bank_account__owner__telegram_id=telegram_id, card_id=card_id)
        .select_related("bank_account")
        .first()
    )
    if card is None:
        raise CardNotFoundError(card_id)

    if card.bank_account.owner.telegram_id != telegram_id:
        raise CardPermissionError(card_id)

    transactions = (
        Transaction.objects.filter(Q(card_from=card) | Q(card_to=card))
        .distinct()
        .values("card_from__card_id", "card_to__card_id", "amount", "time")
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


def get_unred_postcards(telegram_id: (str | int), account_name: str):
    account = BankAccount.objects.filter(owner__telegram_id=telegram_id, name=account_name).first()
    if account is None:
        raise AccountNotFoundError(account_name)

    transactions = Transaction.objects.filter(account_to=account, read=False, has_postcard=True)

    bank_statement = __compile_account_transactions(transactions)
    transactions.update(read=True)

    return bank_statement, round(float(account.money), 2)


def __compile_account_transactions(transactions):
    return [
        {
            "time": t.time.strftime("%d/%m/%Y"),
            "account_from": t.account_from.name,
            "account_to": t.account_to.name,
            "amount": round(float(t.amount), 2),
            "postcard_link": get_presigned_link(t.postcard.name),
        }
        for t in transactions.select_related("account_from", "account_to")
    ]
