from django.db.models import QuerySet

from app.internal.models.bank_account import BankAccount


def create_account(user_info) -> None:
    BankAccount.objects.create(
        owner_id=user_info.id,
        money=0,
    )


def get_accounts(owner_id) -> QuerySet | None:
    """returns QuerySet of accounts if there are any, else None"""

    accounts = BankAccount.objects.filter(owner_id=owner_id)
    if not accounts.exists():
        return None

    return accounts


def get_accounts_info(owner_id) -> dict:
    """return info about accounts if there are any, else empty dict"""

    info = {f"account №{n}": account.money for n, account in enumerate(get_accounts(owner_id))}

    return info
