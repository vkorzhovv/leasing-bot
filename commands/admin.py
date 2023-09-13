from django.contrib import admin
from .models import Command


@admin.register(Command)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'description', 'updated_at')
    list_display_links = ('id', 'key', 'description')
    list_filter = ('updated_at',)
    search_fields = ('key', 'text', 'description')
    readonly_fields=('key',)
    ordering = ('-updated_at',)
