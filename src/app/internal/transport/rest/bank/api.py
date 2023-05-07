from typing import List

from ninja import Router

from app.internal.authentication import AuthBearer
from app.internal.transport.rest.schemas import Message

from . import handlers
from .schemas import BankAccountOut, BankCardSchema, BankStatementAccount, BankStatementCard


def get_bank_accounts_router():
    router = Router(tags=["bank-accounts"])

    router.add_api_operation(
        "",
        ["GET"],
        handlers.bank_status,
        auth=AuthBearer(),
        response={200: List[BankAccountOut]},
    )

    router.add_api_operation(
        "/{str:account_name}",
        ["GET"],
        handlers.get_info,
        auth=AuthBearer(),
        response={200: BankAccountOut},
    )

    router.add_api_operation(
        "/{str:account_name}/send-money",
        ["POST"],
        handlers.send_money_account,
        auth=AuthBearer(),
        response={200: Message},
    )

    router.add_api_operation(
        "/{str:account_name}/bank-statement",
        ["GET"],
        handlers.bank_statement_account,
        auth=AuthBearer(),
        response={200: BankStatementAccount},
    )

    return router


def get_bank_cards_router():
    router = Router(tags=["cards"])

    router.add_api_operation(
        "",
        ["POST"],
        handlers.add_card,
        auth=AuthBearer(),
        response={200: BankCardSchema},
        description="add new card",
    )

    router.add_api_operation(
        "/{int:card_id}/send-money",
        ["POST"],
        handlers.send_money_card,
        auth=AuthBearer(),
        response={200: Message},
        description="send money via card",
    )

    router.add_api_operation(
        "/{int:card_id}/bank-statement",
        ["GET"],
        handlers.bank_statement_card,
        auth=AuthBearer(),
        response={200: BankStatementCard},
        description="get bank statement",
    )

    return router
