import logging
from Bot.models import Key, Captain, Hunter, Queue, Node
from django.db.utils import InterfaceError
from django import db
import random


def already_in(chat_id):
    try:
        hunter = Hunter.objects.get(id=chat_id)
    except Hunter.DoesNotExist:
        return False
    else:
        is_in = hasattr(hunter, "queue")
        if not is_in:
            hunter.delete()
        return is_in


# Create summary of info about a , to_exclude is a list of key (strings) to exclude
def info_summary(chat_id=None, hunter=None, to_exclude=[]):
    lines = []
    key_query_set = Key.objects.all()
    if chat_id is None and hunter is None:
        raise Exception("Entrambi i kwargs impostati a none")
        return None
    if hunter is None:  # if hunter is specified by id
        hunter = Hunter.objects.get(id=chat_id)
    key_list = [key for key in key_query_set if key.name not in to_exclude]
    for key in key_list:
        try:
            value = getattr(hunter, key.name)
            item = f"{key.verbose_name}: {value}"
        except AttributeError:
            logging.debug("", exc_info=True)
        else:
            lines.append(item)
    summary = "\n".join(lines)
    return summary


# update files
def update_info_txt():
    hunter_list = Hunter.objects.all()
    with open("data/players.txt", "w", encoding="utf-8") as out_file:
        out_file.write("INFO SUI PARTECIPANTI:\n")
        for hunter in hunter_list:
            summary = info_summary(hunter=hunter)
            out_file.write(f"{summary}\n\n")


def update_team_txt():
    cap_list = Captain.objects.all()
    with open("data/teams.txt", "w", encoding="utf-8") as out_file:
        out_file.write("COMPOSIZIONE DELLE SQUADRE:\n\n")
        teams_summary = []
        for cap in cap_list:
            hunter_list = cap.hunter_set.all()
            hunter_anag_list = [f"    {anag(hunter)}" for hunter in hunter_list]
            teams_summary.append(
                f"  {cap.anagraphic}:\n" + "    ".join(hunter_anag_list)
            )
        out_file.write("\n\n".join(teams_summary))


# Gives back name & surname
def anag(hunter):
    return f"{hunter.name} {hunter.surname}"


def add_captain(cap_anag, cap_id):
    Captain.objects.create(anagraphic=cap_anag, id=cap_id)


# removes captains of teams containing more than N people
def cap_anag_list(N):
    cap_list = list(Captain.objects.all())
    for cap in cap_list:
        try:
            if len(cap.hunter_set.all()) > N:
                cap_list.remove(cap)
        except KeyError:
            logging.debug("", exc_info=True)
    return [cap.anagraphic for cap in cap_list]
