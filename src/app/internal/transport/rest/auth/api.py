from ninja import Router

from app.internal.transport.rest.schemas import Message

from . import handlers
from .schemas import Token


def get_auth_router():
    router = Router(tags=["auth"])

    router.add_api_operation(
        "/login",
        ["POST"],
        handlers.login,
        response={200: Token},
    )

    router.add_api_operation(
        "/refresh",
        ["POST"],
        handlers.refresh,
        response={200: Token},
    )

    router.add_api_operation(
        "/logout",
        ["POST"],
        handlers.logout,
        response={200: Message},
    )

    return router
