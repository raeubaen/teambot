from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ConversationHandler, Filters, BaseFilter
from Bot.utils import already_in
from .models import Captain, Hunter, Bot_Table, Queue
from emoji import emojize
import random
from .utils import cap_anag_list, info_summary
from .TeamHandling import create_nodes, handle_queue
from bot_site.settings import DEBUG


class Accept:  # BEFORE ASKING ANY DATA
    def make(self, update, context):
        if already_in(update.message.chat_id):
            update.message.reply_text(
                "You are already in"
            )
            return ConversationHandler.END
        _markup = ReplyKeyboardMarkup([["Yes"], ["No"]], one_time_keyboard=True)
        update.message.reply_text("We are still in development")
        update.message.reply_text(
            ""
            " Accept our privacy policy [Yes/No].\n"
            " You can find it at --> link to privacy policy",
            reply_markup=_markup,
        )
        return self.num

    def process(self, update, context):
        if update.message.text == "No":
            update.message.reply_text(
                "To get in accept privacy policy\nTo start again say /start"
            )
            return ConversationHandler.END
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                return txt in ("Yes", "No")
            except AttributeError:
                return False

    filter = Filter()
    key_verbose_name = "Telegram Chat ID"
    key_name = "id"

class Phone:
    def make(self, update, context):
        em1 = emojize(":telephone:", use_aliases=True)
        em2 = emojize(":mobile_phone:", use_aliases=True)
        _contact_button = KeyboardButton(
            text=em1 + " Send your phone number " + em2, request_contact=True
        )
        _markup = ReplyKeyboardMarkup([[_contact_button]], one_time_keyboard=True)
        update.message.reply_text(
            text="Click on the below button",
            reply_markup=_markup,
        )
        return self.num

    def process(self, update, context):
        chat_id = update.message.chat_id
        Hunter.objects.create(id=chat_id, phone=update.message.contact.phone_number)
        return self.make_new(update, context)

    filter = Filters.contact
    key_verbose_name = "Numero di Telefono"
    key_name = "phone"

class Name:
    def make(self, update, context):
        update.message.reply_text("Tell me your name")
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.name = update.message.text
        hunter.save()
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                return all(x.isalpha() or x.isspace() or x == "'" for x in txt)
            except:
                return False

    filter = Filter()
    key_verbose_name = "Nome"
    key_name = "name"

class Surname:
    def make(self, update, context):
        update.message.reply_text("Tell me your surname")
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.surname = update.message.text
        hunter.save()
        return self.make_new(update, context)

    filter = Name.filter
    key_verbose_name = "Cognome"
    key_name = "surname"


class Age:
    def make(self, update, context):
        update.message.reply_text("how old are you? Es. 20")
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.age = int(update.message.text)
        hunter.save()
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                return (txt.isdigit()) and 16 < int(txt) < 40
            except AttributeError:
                return False

    filter = Filter()
    key_verbose_name = "Età"
    key_name = "age"


class Uni:
    def make(self, update, context):
        update.message.reply_text(
            "Do you attend university? Which one? "
        )
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.uni = update.message.text
        hunter.save()
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                return True
            except AttributeError:
                return False

    filter = Filter()
    key_verbose_name = "Università"
    key_name = "uni"


class Time:
    def make(self, update, context):
        update.message.reply_text(
            "Tell me when you will come and when you will go away"
        )
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.tframe = update.message.text
        hunter.save()
        return self.make_new(update, context)

    filter = Uni.filter
    key_verbose_name = "Tempistica"
    key_name = "tframe"

class Perc:
    def make(self, update, context):
        update.message.reply_text(
            "Tell me the probability you come to play (percentage)? Es. 99\n"
        )
        return self.num

    def process(self, update, context):
        hunter = Hunter.objects.get(id=update.message.chat_id)
        hunter.perc = int(update.message.text)
        hunter.save()
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                return txt.isdigit() and 1 <= int(txt) <= 100
            except AttributeError:
                return False

    filter = Filter()
    key_verbose_name = "Probabilità di presenza (%)"
    key_name = "perc"


# Handling the process of assigning a captain
class Grouping:  # others questions are in personalQuestions.py
    def make(self, update, context):
        MAX_MEMBERS_PER_TEAM = Bot_Table.objects.first().max_team_size
        BUTTONS = [[i] for i in cap_anag_list(MAX_MEMBERS_PER_TEAM)]
        random.shuffle(BUTTONS)
        BUTTONS.insert(0, ["Create your team"])
        _markup = ReplyKeyboardMarkup(BUTTONS, one_time_keyboard=True)
        update.message.reply_text("Choose your Captain", reply_markup=_markup)
        return self.num

    def process(self, update, context):
        choice = update.message.text
        hunter = Hunter.objects.get(id=update.message.chat_id)
        if choice == "Create your team":
            update.message.reply_text(
                "Contact the admin. "
                "If you wish to join another team say /stop, then /start e start again."
            )
            queue = Queue.objects.create(situation="Requested own team", hunter=hunter)
            return self.make_new(update, context)
        cap_anag = choice
        queue = Queue.objects.create(situation="waiting", hunter=hunter)
        create_nodes(cap_anag, queue)
        handle_queue(hunter, context)
        return self.make_new(update, context)

    class Filter(BaseFilter):
        def filter(self, message):
            try:
                txt = message.text
                MAX_MEMBERS_PER_TEAM = Bot_Table.objects.first().max_team_size
                flat_buttons = cap_anag_list(MAX_MEMBERS_PER_TEAM)
                flat_buttons.insert(0, "Create your team")
                return txt in flat_buttons
            except AttributeError:
                return False

    filter = Filter()
    key_verbose_name = "Status dell'iscrizione"
    key_name = "queue"


# what happens when conversation_handler.END is triggered
def end_conversation(update, context):
    admin_id = Bot_Table.objects.first().admin_id
    if DEBUG:
        context.bot.send_message(
            chat_id=admin_id,
            text=f"New request:\n{info_summary(chat_id=update.message.chat_id)}",
        )
    update.message.reply_text(
        "Nice, request completed!"
    )
    return ConversationHandler.END


# callback for /stop command
def cancel(update, context):
    try:
      hunter = Hunter.objects.get(id=update.message.chat_id)
      hunter.delete()
    except Hunter.DoesNotExist:
      logging.debug("", exc_info=True)
    update.message.reply_text(
        "All your data has been deleted. To start again say /start"
    )
    return ConversationHandler.END


# question_list = [Phone, Grouping]
question_list = [Phone, Name, Surname, Age, Uni, Time, Perc, Grouping]
question_list.insert(0, Accept)

