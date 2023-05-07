from typing import List

from ninja import Router

from app.internal.authentication import AuthBearer
from app.internal.transport.rest.schemas import Message

from . import handlers
from .schemas import UserSchema


def get_me_router():
    router = Router(tags=["me"])

    router.add_api_operation(
        "",
        ["GET"],
        handlers.get_user,
        auth=AuthBearer(),
        response={200: UserSchema},
        description="get info about yourself",
    )

    router.add_api_operation(
        "",
        ["PUT"],
        handlers.update_user,
        auth=AuthBearer(),
        response={200: Message},
        description="change your info",
    )

    router.add_api_operation(
        "/update-phone",
        ["POST"],
        handlers.update_phone,
        auth=AuthBearer(),
        response={200: Message},
        description="update your phone number",
    )

    router.add_api_operation(
        "/interactions",
        ["GET"],
        handlers.get_interactions,
        auth=AuthBearer(),
        response={200: List[str]},
        description="get list of your interactions",
    )

    return router


def get_friends_router():
    router = Router(tags=["friends"])

    router.add_api_operation(
        "",
        ["POST"],
        handlers.add_friend,
        auth=AuthBearer(),
        response={200: Message},
        description="add someone to friends",
    )

    router.add_api_operation(
        "",
        ["DELETE"],
        handlers.remove_friend,
        auth=AuthBearer(),
        response={200: Message},
        description="remove someone from friends",
    )

    router.add_api_operation(
        "",
        ["GET"],
        handlers.list_friends,
        auth=AuthBearer(),
        response={200: List[str]},
        description="get list of your friends",
    )

    return router
