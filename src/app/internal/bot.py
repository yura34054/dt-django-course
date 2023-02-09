import requests

from config.settings import TELEGRAM_BOT


def setup_webhook():
    if not TELEGRAM_BOT["webhook_mode"]:
        requests.post(TELEGRAM_BOT["telegram_url"] + "setWebhook", data={"url": ""})
        return

    response = requests.post(TELEGRAM_BOT["telegram_url"] + "setWebhook", data=TELEGRAM_BOT["WEBHOOK_INFO"])
    response = response.json()

    if response.get("result", False):
        print("webhook set successfully:", response.get("description"))

    else:
        print("could not setup webhook:", response.get("description"))


def send_message(params):
    return requests.post(TELEGRAM_BOT["telegram_url"] + "sendMessage", data=params)
