import logging

from app.internal.exceptions import ValidationError
from app.internal.services import user_service

logger = logging.getLogger("DT_django_logger")


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
            logger.info(f"user: {update.message.from_user.id}: {func.__name__}")

            func(update, context)

        except ValidationError as e:
            update.message.reply_text(str(e))
            logger.info(f"user: {update.message.from_user.id}: {func.__name__} - {type(e).__name__}")

        except Exception as e:
            update.message.reply_text("Something went wrong, please try again or contact support")
            logger.exception(e)

    return wrapper


def has_arguments(count: int, message: str):
    def decorator(func):
        def wrapper(update, context):
            if len(update.message.text.split()) != count + 1:
                update.message.reply_text(message)
                return

            else:
                func(update, context)

        return wrapper

    return decorator
