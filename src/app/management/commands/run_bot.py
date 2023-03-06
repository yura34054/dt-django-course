from django.core.management.base import BaseCommand

from app.internal import bot


class Command(BaseCommand):
    help = "run telegram bot"

    def handle(self, *args, **options):
        bot.run()
