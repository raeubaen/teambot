from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from Bot.models import Hunter, Captain, Key, Bot_Table
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.http import JsonResponse
from django.views import View
from telegram import Update as telegramUpdate
from telegram import Bot as telegramBot
from Bot.bot_thread import BotUpdateQueue
from django.apps import apps
import Bot.utils as utils
import os
import json
import sys
import logging


@staff_member_required
def reset(request):
    import os
    import sys
    from django.apps import apps

    models = apps.get_app_config("Bot").models
    for mod in models:  # da testare
        models[mod].objects.all().delete()  # da testare
    os.execl(sys.argv[0], *sys.argv)


class webhook(View):
    def post(self, request, *args, **kwargs):
        get_update(request.body)
        return JsonResponse({"ok": "POST request processed"})


def get_update(text):
    bot = telegramBot(Bot_Table.objects.first().token)
    update = telegramUpdate.de_json(json.loads(text), bot)
    update_queue = BotUpdateQueue().queue
    update_queue.put(update)


@login_required
def restart(request):
    os.execl(sys.argv[0], *sys.argv)


def download_players(request):
    utils.update_info_txt()
    file_path = "data/players.txt"
    try:
        wrapper = FileWrapper(open(file_path, "rb"))
        response = HttpResponse(wrapper, content_type="application/force-download")
        response["Content-Disposition"] = "inline; filename=" + os.path.basename(
            file_path
        )
        return response
    except:
        return HttpResponse(status=500)


def download_teams(request):
    utils.update_team_txt()
    file_path = "data/teams.txt"
    try:
        wrapper = FileWrapper(open(file_path, "rb"))
        response = HttpResponse(wrapper, content_type="application/force-download")
        response["Content-Disposition"] = "inline; filename=" + os.path.basename(
            file_path
        )
        return response
    except:
        return HttpResponse(status=500)


@login_required
def add_captain(request):
    return render(request, "add_captain.html")


@login_required
def send_add_captain(request):
    from Bot.utils import add_captain

    cap_anag = request.POST.get("cap_name")
    cap_id = int(request.POST.get("cap_id"))
    add_captain(cap_anag, cap_id)
    return redirect("home")


def home(request):
    return render(request, "home.html")
