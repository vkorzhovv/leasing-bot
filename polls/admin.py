from django.contrib import admin
from .models import Poll, PollMedia, PollOptions


class PollMediaInline(admin.StackedInline):
    model = PollMedia
    extra = 1  # Количество дополнительных полей для добавления
    readonly_fields = ('absolute_media_path',)

class PollOptionsInline(admin.StackedInline):
    model = PollOptions
    extra = 1  # Количество дополнительных полей для добавления


@admin.register(Poll)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'group', 'approved', 'created_at')
    list_filter = ('created_at', 'approved', 'group')
    search_fields = ('title', 'approved')
    ordering = ('approved',)
    readonly_fields=('user', 'approved')
    inlines = [PollOptionsInline, PollMediaInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk: # call super method if object has no primary key
            if not obj.user:
                obj._context_user = request.user
                #super(BotUserAdmin, self).save_model(request, obj, form, change)
            super(BotUserAdmin, self).save_model(request, obj, form, change)
        else:
            pass # don't actually save the parent instance

    def save_formset(self, request, form, formset, change):
        formset.save() # this will save the children
        if formset.model == PollMedia:
            form.instance.save() # form.instance is the parent
