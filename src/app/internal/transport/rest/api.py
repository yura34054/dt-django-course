from ninja import NinjaAPI

from app.internal.exceptions.validation_errors import CardPermissionError, UnauthorizedRequest, ValidationError

from .auth.api import get_auth_router
from .bank.api import get_bank_accounts_router, get_bank_cards_router
from .users.api import get_friends_router, get_me_router


def get_api():
    api = NinjaAPI(
        version="0.0.1",
    )

    api.add_router("/me", get_me_router())
    api.add_router("/friends", get_friends_router())
    api.add_router("/bank-accounts", get_bank_accounts_router())
    api.add_router("/bank-cards", get_bank_cards_router())
    api.add_router("/auth", get_auth_router())

    @api.exception_handler(UnauthorizedRequest)
    def on_invalid_token(request, exc):
        return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)

    @api.exception_handler(CardPermissionError)
    def on_forbidden(request, exc):
        return api.create_response(request, {"detail": "Forbidden"}, status=403)

    @api.exception_handler(ValidationError)
    def on_bad_request(request, exc):
        return api.create_response(request, {"detail": "Invalid request", "error": type(exc).__name__}, status=400)

    return api
