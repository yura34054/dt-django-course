from app.internal.bot import send_message
from app.internal.services import user_service


def start(context):
    user_service.create_user(context["user"])

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

    user = user_service.get_user(chat_id=context["user"]["id"])
    user_service.update_user_phone(user, context["contact"]["phone_number"])

    params = {"chat_id": context["user"]["id"], "text": "Thanks", "reply_markup": '{"remove_keyboard":true}'}
    send_message(params)


def me(context):
    user = user_service.get_user(chat_id=context["user"]["id"]).get()
    params = {"chat_id": user.chat_id, "text": "to use this method you need to provide your phone (/set_phone)"}

    user_info = user_service.get_user_info(user)

    if len(user_info) == 0:
        send_message(params)
        return

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
