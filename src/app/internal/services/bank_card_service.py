from django.db.models import QuerySet

from app.internal.models.bank_account import BankAccount
from app.internal.models.bank_card import BankCard


def __get_cards(owner_id) -> QuerySet | None:
    """returns QuerySet of accounts if there are any, else None"""

    cards = BankCard.objects.filter(bankcard__owner_id=owner_id)

    return cards


# def get_cards_info(owner_id) -> dict:
#     """return info about accounts if there are any, else empty dict"""
#
#     info = {f"Card {n}": card.bank_account.account_id for n, card in enumerate(__get_cards(owner_id))}
#
#     return info
