from django.contrib import admin
from .models import StoryNews


@admin.register(StoryNews)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_manager', 'description', 'created_at', 'sort', 'approved', 'position')
    list_filter = ('created_at', 'sort', 'approved')
    search_fields = ('name', 'description', 'created_at', 'sort')
    ordering = ('-created_at',)
    readonly_fields=('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj._context_user = request.user
        super().save_model(request, obj, form, change)
