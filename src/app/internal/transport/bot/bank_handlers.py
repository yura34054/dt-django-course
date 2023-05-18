from telegram import Update
from telegram.ext import CallbackContext

from app.internal.decorators.telegram_decorators import has_arguments, logged, requires_phone
from app.internal.services import bank_service


@requires_phone
@has_arguments(1, "Use this command with one parameter: /bank_account_info {account name}")
@logged
def bank_account_info(update: Update, context: CallbackContext):
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

    update.message.reply_text("\n".join((f'{account["name"]}: {account["money"]}' for account in info)))


@requires_phone
@has_arguments(1, "Use this command with one parameter: /add_account {account name}")
@logged
def add_account(update: Update, context: CallbackContext):
    name = update.message.text.split()[1]

    bank_service.create_account(update.message.from_user.id, name)
    update.message.reply_text(f'Account "{name}" successfully created')


@requires_phone
@has_arguments(
    2,
    "Use this command with four parameters: " "/change_or_create_account {account name} {new name}",
)
@logged
def change_or_create_account(update: Update, context: CallbackContext):
    name, new_name = update.message.text.split()[1:]

    if bank_service.change_or_create_account(update.message.from_user.id, name, new_name) == "created":
        update.message.reply_text(f'Account "{new_name}" successfully created')
        return

    update.message.reply_text(f'Account "{name}" successfully updated')


@requires_phone
@has_arguments(1, "Use this command with one parameter: /add_card {account name}")
@logged
def add_card(update: Update, context: CallbackContext):
    bank_account_name = update.message.text.split()[1]

    card_id = bank_service.create_card(update.message.from_user.id, bank_account_name)
    update.message.reply_text(f'Card "{card_id}" successfully created')


@requires_phone
@has_arguments(
    4,
    "Use this command with four parameters: "
    "/send_money_account {receiver username} {your account name} {receiver account name} {amount}",
)
@logged
def send_money_account(update: Update, context: CallbackContext):
    receiver_username, account_name, receiver_account_name, amount = update.message.text.split()[1:]

    amount = bank_service.send_money_account(
        update.message.from_user.id, receiver_username, account_name, receiver_account_name, amount
    )
    update.message.reply_text(f"Successfully sent {amount} to @{receiver_username}")


@requires_phone
@has_arguments(3, "Use this command with three parameters: /send_money_card {your card id} {receiver card id} {amount}")
@logged
def send_money_card(update: Update, context: CallbackContext):
    card_id, receiver_card_id, amount = update.message.text.split()[1:]

    amount = bank_service.send_money_card(update.message.from_user.id, card_id, receiver_card_id, amount)
    update.message.reply_text(f'Successfully sent {amount} to card "{receiver_card_id}"')


@requires_phone
@has_arguments(1, "Use this command with one parameter: /get_bank_statement_account {account_name}")
@logged
def get_bank_statement_account(update: Update, context: CallbackContext):
    account_name = update.message.text.split()[1]

    bank_statement, money = bank_service.get_bank_statement_account(update.message.from_user.id, account_name)
    if not bank_statement:
        update.message.reply_text(f"No transactions for account {account_name} found" + f"\nYour balance: {money}")

    update.message.reply_text(
        "\n".join(f"{st['time']}: {st['account_from']} -> {st['account_to']} | {st['amount']}" for st in bank_statement)
        + f"\nYour balance: {money}"
    )


@requires_phone
@has_arguments(1, "Use this command with one parameter: /get_bank_statement_card {card_id}")
@logged
def get_bank_statement_card(update: Update, context: CallbackContext):
    card_id = update.message.text.split()[1]

    bank_statement, money = bank_service.get_bank_statement_card(update.message.from_user.id, card_id)
    if not bank_statement:
        update.message.reply_text(f'No transactions for card "{card_id}" found' + f"\nYour balance: {money}")

    update.message.reply_text(
        "\n".join(f"{st['time']}: {st['account_from']} -> {st['account_to']} | {st['amount']}" for st in bank_statement)
        + f"\nYour balance: {money}"
    )
