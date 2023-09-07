from django.contrib import admin
from .models import Poll, PollMedia


class PollMediaInline(admin.StackedInline):
    model = PollMedia
    extra = 1  # Количество дополнительных полей для добавления
    readonly_fields = ('absolute_media_path',)


@admin.register(Poll)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'group', 'approved', 'created_at')
    list_filter = ('created_at', 'approved', 'group')
    search_fields = ('title', 'text', 'approved')
    ordering = ('approved',)
    readonly_fields=('user',)
    inlines = [PollMediaInline]

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj._context_user = request.user
        super().save_model(request, obj, form, change)
