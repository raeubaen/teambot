from django.apps import AppConfig
import sys
import logging
from .bot_config import bot_config
from telegram import Bot as telegramBot
from bot_site.settings import DEBUG


class adminHandler(logging.Handler):
    def __init__(self, token=None, admin_id=None):
        self.bot = telegramBot(token)
        self.admin_id = admin_id
        logging.Handler.__init__(self)

    def emit(self, record):
        self.bot.send_message(chat_id=self.admin_id, text=self.format(record))


class BotConfig(AppConfig):
    name = "Bot"

    def ready(self):
        if not (
            set(sys.argv)
            & set(
                [
                    "makemigrations",
                    "migrate",
                    "collectstatic",
                    "createsuperuser",
                    "shell",
                ]
            )
        ):
            import Bot.bot_thread as bot_thread
            from .models import Bot_Table
            from .exceptions import UniqueObjectError

            if not Bot_Table.objects.exists():
                try:
                    Bot_Table.objects.create(**bot_config)
                except UniqueObjectError:
                    logging.debug("", exc_info=True)
            bot = Bot_Table.objects.first()
            _hd = adminHandler(token=bot.token, admin_id=bot.admin_id)
            level = logging.ERROR
            _hd.setLevel(level)
            if not DEBUG:
                logging.getLogger("").addHandler(_hd)

            bot_thread.run()
