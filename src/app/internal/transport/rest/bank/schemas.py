from typing import List

from ninja import Schema


class BankCardSchema(Schema):
    card_id: int


class BankAccountSchema(Schema):
    name: str


class BankAccountIn(BankAccountSchema):
    owner: str


class BankAccountOut(BankAccountSchema):
    money: str
    cards: List[int] = None


class TransactionAccount(Schema):
    time: str
    account_from: str
    account_to: str
    amount: float


class TransactionCard(Schema):
    time: str
    card_from: int
    card_to: int
    amount: float


class BankStatementAccount(Schema):
    transactions: List[TransactionAccount] = None
    money: float


class BankStatementCard(Schema):
    transactions: List[TransactionCard] = None
    money: float
