import logging
import sys
from telegram.ext import Dispatcher
from queue import Queue
from telegram import Bot
from telegram.ext import CommandHandler, CallbackQueryHandler
import threading
from bot_site.settings import DEBUG, SITE_ADDRESS
import requests
from .models import Bot_Table
from .TeamHandling import cap_queue_callback
from .models import Captain


def not_hand_exc(exctype, value, trace_back):
    logging.error(
        "Uncaught Exception: Warning!!", exc_info=(exctype, value, trace_back)
    )


def error(update, context):
    try:
        raise context.error
    except Exception:  # to log almost all exceptions
        logging.exception(f"Update: {update}")


sys.excepthook = not_hand_exc

# implements Singleton pattern - boring
class BotUpdateQueue(object):
    class __BotUpdateQueue:
        def __init__(self):
            self.queue = None

        def __str__(self):
            return str(self)

    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not BotUpdateQueue.instance:
            BotUpdateQueue.instance = BotUpdateQueue.__BotUpdateQueue()
        return BotUpdateQueue.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


# callback for /id command
def get_id(update, context):
    update.message.reply_text(
        f"Il tuo chat_id con questo bot è: {update.message.chat_id}"
    )


def set_webhook(token):
    if not DEBUG:  # in production
        webhook_url = f"https://{SITE_ADDRESS}/bot/"
    if DEBUG:  # in localhost
        from pyngrok import ngrok
        ngrok_url = ngrok.connect(port=8000)
        webhook_url = ngrok_url.replace("http", "https") + "/bot/"

    req = requests.post(
        "https://api.telegram.org/bot" + token + "/setWebhook", {"url": webhook_url}
    )
    if req.status_code != 200:
        logging.error("Webhook not set!")


def run():
    from .Conversation import conv_handler, cancel

    # importing data from database
    bot_db_table = Bot_Table.objects.first()
    token = bot_db_table.token

    # initializing
    bot = Bot(token)
    update_queue = Queue()
    BotUpdateQueue().queue = update_queue
    dp = Dispatcher(bot, update_queue, use_context=True)

    if not Captain.objects.all():  # if db does not contain captains
        with open(
            "captains.txt", "r", encoding="utf-8"
        ) as in_file:  # cap1_name - cap1_id, ...
            entries = in_file.read().replace("\n", "").split(",")
        for entry in entries:
            anagraphic, id_str = entry.split(" - ")
            id = int(id_str)
            Captain.objects.create(id=id, anagraphic=anagraphic)

    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CallbackQueryHandler(cap_queue_callback))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("stop", cancel))
    dp.add_error_handler(error)

    thread = threading.Thread(target=dp.start, name="dispatcher")
    thread.start()

    set_webhook(token)


if __name__ == "__main__":
    run()
