from django.contrib import admin
from .models import Post, PostMedia


class PostMediaInline(admin.StackedInline):
    model = PostMedia
    extra = 1  # Количество дополнительных полей для добавления
    readonly_fields = ('absolute_media_path',)


@admin.register(Post)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'group', 'approved', 'created_at')
    list_filter = ('created_at', 'approved', 'group')
    search_fields = ('text', 'approved')
    ordering = ('approved',)
    readonly_fields=('user',)
    inlines = [PostMediaInline]

    # def save_model(self, request, obj, form, change):
    #     if not obj.user:
    #         obj._context_user = request.user
    #     super().save_model(request, obj, form, change)



    def save_model(self, request, obj, form, change):
        if not obj.pk: # call super method if object has no primary key
            if not obj.user:
                obj._context_user = request.user
                # super(BotUserAdmin, self).save_model(request, obj, form, change)
            super(BotUserAdmin, self).save_model(request, obj, form, change)
        else:
            pass # don't actually save the parent instance

    def save_formset(self, request, form, formset, change):
        formset.save() # this will save the children
        if formset.model == PostMedia:
            form.instance.save() # form.instance is the parent
