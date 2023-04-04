from queue import Queue
from threading import Thread

from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler

from app.internal.transport import bot
from config.settings import TELEGRAM_BOT


def setup():
    # Create bot, update queue and dispatcher instances
    telegram_bot = Bot(TELEGRAM_BOT["bot_token"])
    telegram_bot.set_webhook(
        url=TELEGRAM_BOT["webhook_url"],
        drop_pending_updates=TELEGRAM_BOT["drop_pending_updates"],
        secret_token=TELEGRAM_BOT["secret_token"],
    )

    update_queue = Queue()

    dispatcher = Dispatcher(telegram_bot, update_queue)

    # Register handlers
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

    # Start the thread
    thread = Thread(target=dispatcher.start, name="dispatcher")
    thread.daemon = True  # I DO NOT UNDERSTAND HOW THIS WORKS
    thread.start()

    return telegram_bot, update_queue


telegram_bot, update_queue = setup()
