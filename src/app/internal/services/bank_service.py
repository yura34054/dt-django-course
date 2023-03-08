from django.db.models import Q, QuerySet

from app.internal.models.bank_account import BankAccount


def create_account(user_info) -> None:
    BankAccount.objects.create(
        owner_id=user_info.id,
        money=0,
    )


def get_accounts(owner_id=None) -> QuerySet | None:
    """returns QuerySet of accounts if there are any, else None"""

    accounts = BankAccount.objects.filter(owner_id=owner_id)
    if not accounts.exists():
        return None

    return accounts


def get_accounts_info(accounts: QuerySet) -> dict:
    """return info about user if he has his phone set, else empty dict"""

    info = {f"account No:{n}": account.money for n, account in enumerate(accounts)}

    return info
