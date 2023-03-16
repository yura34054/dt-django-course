from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app.internal.transport.bot import handlers
from config.settings import TELEGRAM_BOT


def run() -> None:
    updater = Updater(TELEGRAM_BOT["bot_token"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handlers.start))
    dispatcher.add_handler(CommandHandler("set_phone", handlers.set_phone))
    dispatcher.add_handler(MessageHandler(Filters.contact, handlers.update_user_phone))
    dispatcher.add_handler(CommandHandler("me", handlers.me))
    dispatcher.add_handler(CommandHandler("bank_status", handlers.bank_status))

    updater.start_polling()

    updater.idle()
