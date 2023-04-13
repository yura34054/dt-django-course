from telegram import Update
from telegram.ext import CallbackContext

from app.internal.decorators.telegram_decorators import logged, requires_phone
from app.internal.services import bank_service


@requires_phone
@logged
def bank_account_info(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: /bank_account_info {account name}")
        return

    name = update.message.text.split()[1]
    info = bank_service.get_account_info(update.message.from_user.id, name)

    if info == {}:
        update.message.reply_text(f"Account {name} not found")
        return

    update.message.reply_text("\n".join((f"{param}: {value}" for param, value in info.items())))


@requires_phone
@logged
def bank_status(update: Update, context: CallbackContext):
    info = bank_service.get_accounts(update.message.from_user.id)

    if info == {}:
        update.message.reply_text("No accounts found")
        return

    update.message.reply_text("\n".join((f"{param}: {value}" for param, value in info.items())))


@requires_phone
@logged
def add_account(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: /add_account {account name}")
        return

    name = update.message.text.split()[1]

    update.message.reply_text(bank_service.create_account(update.message.from_user.id, name))


@requires_phone
@logged
def add_card(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: /add_card {account name}")
        return

    bank_account_name = update.message.text.split()[1]

    update.message.reply_text(bank_service.create_card(update.message.from_user.id, bank_account_name))


@requires_phone
@logged
def send_money_account(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 5:
        update.message.reply_text(
            "Use this command with four parameters: "
            "/send_money_account {receiver username} {your account name} {receiver account name} {amount}"
        )
        return

    update.message.reply_text(
        bank_service.send_money_account(update.message.from_user.id, *update.message.text.split()[1:])
    )


@requires_phone
@logged
def send_money_card(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 4:
        update.message.reply_text(
            "Use this command with three parameters: " "/send_money_card {your card id} {receiver card id} {amount}"
        )
        return

    update.message.reply_text(
        bank_service.send_money_card(update.message.from_user.id, *update.message.text.split()[1:])
    )


@requires_phone
@logged
def get_bank_statement_account(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: " "/get_bank_statement_account {account_name}")
        return

    data = bank_service.get_bank_statement_account(update.message.from_user.id, update.message.text.split()[1])
    if isinstance(data, str):
        update.message.reply_text(data)
        return
    bank_statement, money = data

    update.message.reply_text(
        "\n".join(f"{st['time']}: {st['account_from']} -> {st['account_to']} | {st['amount']}" for st in bank_statement)
        + f"\nYour balance: {money}"
    )


@requires_phone
@logged
def get_bank_statement_card(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: " "/get_bank_statement_card {card_id}")
        return

    data = bank_service.get_bank_statement_card(update.message.from_user.id, update.message.text.split()[1])
    if isinstance(data, str):
        update.message.reply_text(data)
        return
    bank_statement, money = data

    update.message.reply_text(
        "\n".join(f"{st['time']}: {st['card_from']} -> {st['card_to']} | {st['amount']}" for st in bank_statement)
        + f"\nYour balance: {money}"
    )
