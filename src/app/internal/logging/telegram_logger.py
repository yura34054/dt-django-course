import logging

import telegram


class TelegramLogHandler(logging.Handler):
    def __init__(self, logging_telegram_token, logging_chat_id):
        super().__init__()

        self.bot = telegram.Bot(logging_telegram_token)
        self.chat = logging_chat_id

    def emit(self, record):
        self.bot.send_message(self.chat, record.getMessage())
