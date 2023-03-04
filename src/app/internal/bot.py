import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app.internal.services.telegram_service import me, set_phone, start, update_user_phone
from config.settings import TELEGRAM_BOT


def run() -> None:
    updater = Updater(TELEGRAM_BOT["bot_token"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_phone", set_phone))
    dispatcher.add_handler(MessageHandler(Filters.contact, update_user_phone))
    dispatcher.add_handler(CommandHandler("me", me))

    updater.start_polling()

    updater.idle()
