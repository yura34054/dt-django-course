from django.apps import AppConfig as Config

from app.internal.bot import setup_webhook


class AppConfig(Config):
    name = "app"

    def ready(self) -> None:
        setup_webhook()


default_app_config = "app.AppConfig"
