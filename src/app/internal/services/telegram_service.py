from app.internal.bot import send_message
from app.internal.models.user import User


def start(context):
    user_info = context["user"]
    if User.objects.filter(chat_id=user_info["id"]).exists():
        return

    User.objects.create(
        chat_id=user_info["id"],
        first_name=user_info["first_name"],
        last_name=user_info.get("last_name", ""),
        username=user_info.get("username", ""),
    )

    params = {
        "chat_id": context["user"]["id"],
        "text": "Hi!",
    }
    send_message(params)


def set_phone(context):
    params = {
        "chat_id": context["user"]["id"],
        "text": "Give me your phone number",
        "reply_markup": '{"keyboard":[[{"text":"Send phone number","request_contact":true}]]}',
    }
    send_message(params)


def update_user_phone(context):
    if context["user"]["id"] != context["contact"].get("user_id"):
        return

    User.objects.filter(chat_id=context["user"]["id"]).update(phone_number=context["contact"]["phone_number"])

    params = {"chat_id": context["user"]["id"], "text": "Thanks", "reply_markup": '{"remove_keyboard":true}'}
    send_message(params)


def me(context):
    user = User.objects.get(chat_id=context["user"]["id"])
    params = {"chat_id": user.chat_id, "text": "to use this method you need to provide your phone (/set_phone)"}

    if user.phone_number is None:
        send_message(params)
        return

    user_info = {
        "First_name": user.first_name,
        "Last_name": user.last_name,
        "Username": user.username,
        "Phone_number": user.phone_number,
    }

    params["text"] = "\n".join((f"{param}: {value}" for param, value in user_info.items()))
    send_message(params)


def handle_message(context):
    if context["contact"] is not None:
        update_user_phone(context)


def handle_command(context):
    match context["text"]:
        case "/start":
            start(context)

        case "/set_phone":
            set_phone(context)

        case "/me":
            me(context)

        case _:
            pass


def handle_update(update: dict):
    if "message" in update:
        context = {
            "user": update["message"].get("from"),
            "text": update["message"].get("text", ""),
            "contact": update["message"].get("contact"),
        }

        if context["text"].startswith("/"):
            handle_command(context)

        else:
            handle_message(context)
