from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from app.internal.decorators.telegram_decorators import logged, requires_phone
from app.internal.exceptions import ValidationError
from app.internal.services import user_service


@logged
def start(update: Update, context: CallbackContext):
    from_user = update.message.from_user
    user_service.create_user(
        from_user.id,
        from_user.first_name,
        from_user.last_name,
        from_user.username,
    )
    update.message.reply_text("Hi!")


@logged
def set_phone(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Give me your phone number",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Send phone number", request_contact=True)]]),
    )


@logged
def update_user_phone(update: Update, context: CallbackContext):
    if update.message.from_user.id != update.message.contact.user_id:
        return

    user_service.update_user_phone(update.message.from_user.id, update.message.contact.phone_number)

    update.message.reply_text(
        "Thanks",
        reply_markup=ReplyKeyboardRemove(),
    )


@requires_phone
@logged
def me(update: Update, context: CallbackContext):
    user_info = user_service.get_user_info(telegram_id=update.message.from_user.id)

    update.message.reply_text("\n".join((f"{param}: {value}" for param, value in user_info.items())))


@requires_phone
@logged
def add_friend(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: " "/add_friend {friend username}")
        return

    friend_username = update.message.text.split()[1]

    try:
        user_service.add_friend(update.message.from_user.id, friend_username)
        update.message.reply_text(f"@{friend_username} added to friends")

    except ValidationError as e:
        update.message.reply_text(str(e))


@requires_phone
@logged
def remove_friend(update: Update, context: CallbackContext):
    if len(update.message.text.split()) != 2:
        update.message.reply_text("Use this command with one parameter: " "/remove_friend {friend username}")
        return

    friend_username = update.message.text.split()[1]

    try:
        user_service.remove_friend(update.message.from_user.id, friend_username)
        update.message.reply_text(f"@{friend_username} removed from friends")

    except ValidationError as e:
        update.message.reply_text(str(e))


@requires_phone
@logged
def list_friends(update: Update, context: CallbackContext):
    friends = user_service.list_friends(update.message.from_user.id)

    if len(friends) == 0:
        update.message.reply_text("No friends found :(")
        return

    update.message.reply_text("Your friends:\n" + ", ".join(friends))


@requires_phone
@logged
def get_interactions(update: Update, context: CallbackContext):
    update.message.reply_text(", ".join(user_service.get_interactions(update.message.from_user.id)))
