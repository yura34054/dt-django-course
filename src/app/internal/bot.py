import requests

from config.settings import TELEGRAM_BOT


def setup_webhook():
    requests.post(TELEGRAM_BOT["telegram_url"] + "setWebhook", data=TELEGRAM_BOT["WEBHOOK_INFO"])


def send_message(params):
    return requests.post(TELEGRAM_BOT["telegram_url"] + "sendMessage", data=params)
