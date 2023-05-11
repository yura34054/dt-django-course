import logging

from app.internal.exceptions import ValidationError
from app.internal.services import user_service

logging.basicConfig(level=logging.INFO)


def requires_phone(func):
    def wrapper(update, context):
        if not user_service.is_phone_set(telegram_id=update.message.from_user.id):
            update.message.reply_text("To use this method you need to provide your phone (/set_phone)")

        else:
            func(update, context)

    return wrapper


def logged(func):
    def wrapper(update, context):
        try:
            logging.info("user: {id}: {function}".format(id=update.message.from_user.id, function=func.__name__))

            func(update, context)

        except ValidationError as e:
            update.message.reply_text(str(e))

        except Exception as e:
            update.message.reply_text("Something went wrong, please try again or contact support")
            logging.exception(e)

    return wrapper


def has_arguments(count: int, message: str):
    def decorator(func):
        def wrapper(update, context):
            if (update.message.text is not None and len(update.message.text.split()) == count + 1) or (
                update.message.caption is not None and len(update.message.caption.split()) == count + 1
            ):
                func(update, context)

            else:
                update.message.reply_text(message)
                return

        return wrapper

    return decorator
