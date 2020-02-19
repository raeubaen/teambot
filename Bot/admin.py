from django.contrib import admin

# Register your models here.
from .models import Captain, Queue, Hunter, Key, Bot_Table

class Hunter_Inline(admin.StackedInline):
    model = Hunter

class Queue_Inline(admin.StackedInline):
    model = Queue

class Captain_Admin(admin.ModelAdmin):
    inlines = [
        Hunter_Inline,
    ]

class Hunter_Admin(admin.ModelAdmin):
    inlines = [
        Queue_Inline,
    ]

admin.site.register(Captain, Captain_Admin)
admin.site.register(Hunter, Hunter_Admin)
admin.site.register(Key)
admin.site.register(Bot_Table)

