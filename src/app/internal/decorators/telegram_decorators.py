import logging

from app.internal.services import user_service

logging.basicConfig(level=logging.INFO)


def requires_phone(func):
    def wrapper(update, context):
        user = user_service.get_user(telegram_id=update.message.from_user.id)

        if user.phone_number == "":
            update.message.reply_text("To use this method you need to provide your phone (/set_phone)")

        else:
            func(update, context)

    return wrapper


def logged(func):
    def wrapper(update, context):
        try:
            logging.info("user: {id}: {function}".format(id=update.message.from_user.id, function=func.__name__))

            return func(update, context)

        except Exception as e:
            update.message.reply_text("Something went wrong, please try again or contact support")
            logging.exception(e)

    return wrapper
