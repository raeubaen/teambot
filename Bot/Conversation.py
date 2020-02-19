from telegram.ext import MessageHandler, Filters, ConversationHandler, CommandHandler
from .Questions import Accept, Phone, Name, Surname, Age, Uni, Time, Perc, Grouping, end_conversation, cancel, question_list
from .models import Key, Hunter, Bot_Table
import logging

def istances(
    classes_list
):  # makes the conv handler work - connects make, process and new questions
    ist = [cls() for cls in classes_list]
    for i in range(len(ist)):
        ist[i].num = i
        try:
            ist[i].make_new = ist[i + 1].make
        except IndexError:
            ist[i].make_new = end_conversation
    return ist


def states(istances):  # sets the Conversational Handler
    stg = {}
    for ist in istances:
        stg[ist.num] = [
            MessageHandler(ist.filter, ist.process),
            CommandHandler("stop", cancel),
            MessageHandler(~ist.filter, ist.make),
        ]
    return stg


def create_key_list(ist_list):  # gives back a list of keys contained in classes
    key_list = []
    for ist in ist_list:
        try:
            key_list.append({
                "name": ist.key_name,
                "verbose_name": ist.key_verbose_name})
        except AttributeError:
            logging.debug("", exc_info=True)
    return key_list

ist = istances(question_list)

key_list = create_key_list(ist)
Key.objects.all().delete()
for key in key_list:
    Key.objects.create(**key)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", ist[0].make)],
    states=states(ist),
    fallbacks=[CommandHandler("stop", cancel)],
)
