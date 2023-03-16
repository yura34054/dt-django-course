from django.db.models import QuerySet

from app.internal.models.bank_account import BankAccount


def create_account(user_info) -> None:
    BankAccount.objects.create(
        owner_id=user_info.id,
        account_id=len(__get_accounts(user_info.id)),
        money=0,
    )


def __get_accounts(owner_id) -> QuerySet:
    """returns QuerySet of accounts if there are any, else None"""

    accounts = BankAccount.objects.filter(owner_id=owner_id)

    return accounts


def get_accounts_info(owner_id) -> list:
    """return info about accounts if there are any, else empty list"""

    info = [
        f"account №{account.account_id}: {account.money}; cards: {account.bankcard_set.count()}"
        for account in __get_accounts(owner_id)
    ]

    return info
