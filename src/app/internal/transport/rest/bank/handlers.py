from app.internal.services import bank_service

from .schemas import BankAccountIn, BankAccountSchema, BankCardSchema


def bank_status(request):
    return bank_service.get_accounts(request.auth)


def get_info(request, account_name):
    return bank_service.get_account_info(request.auth, account_name)


def send_money_account(request, account_name, amount: float, account_to: BankAccountIn):
    bank_service.send_money_account(request.auth, account_to.owner, account_name, account_to.name, amount)
    return {"message": "money sent successfully"}


def bank_statement_account(request, account_name):
    transactions, money = bank_service.get_bank_statement_account(request.auth, account_name)
    return {"transactions": transactions, "money": money}


def add_card(request, account: BankAccountSchema):
    return bank_service.create_card(request.auth, account.name)


def send_money_card(request, card_id, amount: float, card_to: BankCardSchema):
    bank_service.send_money_card(request.auth, card_id, card_to.id, amount)
    return {"message": "money sent successfully"}


def bank_statement_card(request, card_id):
    transactions, money = bank_service.get_bank_statement_card(request.auth, card_id)
    return {"transactions": transactions, "money": money}
