from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from app.internal.transport import bot
from config.settings import TELEGRAM_BOT


def run() -> None:
    updater = Updater(TELEGRAM_BOT["bot_token"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", bot.start))
    dispatcher.add_handler(CommandHandler("set_phone", bot.set_phone))
    dispatcher.add_handler(MessageHandler(Filters.contact, bot.update_user_phone))
    dispatcher.add_handler(CommandHandler("me", bot.me))

    dispatcher.add_handler(CommandHandler("add_friend", bot.add_friend))
    dispatcher.add_handler(CommandHandler("remove_friend", bot.remove_friend))
    dispatcher.add_handler(CommandHandler("list_friends", bot.list_friends))

    dispatcher.add_handler(CommandHandler("add_account", bot.add_account))
    dispatcher.add_handler(CommandHandler("add_card", bot.add_card))
    dispatcher.add_handler(CommandHandler("bank_account_info", bot.bank_account_info))
    dispatcher.add_handler(CommandHandler("bank_status", bot.bank_status))
    dispatcher.add_handler(CommandHandler("send_money", bot.send_money))

    updater.start_polling()

    updater.idle()
