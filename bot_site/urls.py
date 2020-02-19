from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
import bot_site.views as views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home, name="home"),
    # actions in home (mainWindow)
    path("download_players/", views.download_players, name="download_players"),
    path("download_teams/", views.download_teams, name="download_teams"),
    path("restart/", views.restart, name="restart"),
    path("add_captain/", views.add_captain, name="add_captain"),
    path("send_add_captain/", views.send_add_captain, name="send_add_captain"),
    path("reset/", views.reset, name="reset"),
    path("bot/", csrf_exempt(views.webhook.as_view())),
]
