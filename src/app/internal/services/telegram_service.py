from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from app.internal.services import bank_service, user_service


def start(update: Update, context: CallbackContext):
    user_service.create_user(update.message.from_user)
    update.message.reply_text("Hi!")


def set_phone(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Give me your phone number",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Send phone number", request_contact=True)]]),
    )


def update_user_phone(update: Update, context: CallbackContext):
    if update.message.from_user.id != update.message.contact.user_id:
        return

    user = user_service.get_user(telegram_id=update.message.from_user.id)
    user_service.update_user_phone(user, update.message.contact.phone_number)

    update.message.reply_text(
        "Thanks",
        reply_markup=ReplyKeyboardRemove(),
    )


def me(update: Update, context: CallbackContext):
    user = user_service.get_user(telegram_id=update.message.from_user.id)
    user_info = user_service.get_user_info(user)

    if len(user_info) == 0:
        update.message.reply_text("To use this method you need to provide your phone (/set_phone)")
        return

    update.message.reply_text("\n".join((f"{param}: {value}" for param, value in user_info.items())))


def bank_status(update: Update, context: CallbackContext):
    accounts = bank_service.get_accounts(owner_id=update.message.from_user.id)
    if accounts is None:
        update.message.reply_text("No bank accounts found")
        return

    info = bank_service.get_accounts_info(accounts)

    update.message.reply_text("\n".join((f"{param}: {value}" for param, value in info.items())))
