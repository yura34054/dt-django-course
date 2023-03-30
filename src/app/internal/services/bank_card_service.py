from django.db.models import Q, QuerySet

from app.internal.models.bank_account import BankAccount
from app.internal.models.bank_card import BankCard
from app.internal.services.bank_account_service import create_account, get_account
from app.internal.services.user_service import get_user


def create_card(user_info, bank_account_name, name):
    """create new BankCard object if possible, return reply message"""

    bank_account = get_account(user_info.id, bank_account_name)

    if bank_account is None:
        return f'No account "{bank_account_name}" found'

    if get_card(bank_account_name, name) is not None:
        return f'Card "{name}" already exists'

    BankCard.objects.create(
        bank_account=bank_account,
        name=name,
    )

    return f'Card "{name}" successfully created'


def get_card(bank_account_name, name):
    """returns BankCard object if bank account exists, else None"""

    account = BankCard.objects.filter(Q(bank_account__name=bank_account_name) & Q(name=name))

    if not account.exists():
        return None

    return account.get()
