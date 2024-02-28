from django.contrib import admin
from .models import BotUser, BotUserGroup, ExtendedUser
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from import_export.admin import ExportActionModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export.formats.base_formats import DEFAULT_FORMATS
from products.formats import XML
from django.contrib import messages



@admin.register(BotUser)
class BotUserAdmin(ExportActionModelAdmin):
    formats = DEFAULT_FORMATS + [XML]
    list_display = ('user_id', 'name', 'city', 'company_name', 'phone', 'activated', 'created_at', 'last_interaction', 'display_groups')
    list_filter = ('phone', 'activated')
    search_fields = ('name', 'company_name', 'phone')
    ordering = ('-created_at',)


    def save_model(self, request, obj, form, change):
        username = form.cleaned_data.get('username', None)
        if 'manager' in form.changed_data and form.cleaned_data['manager'] and username==None:
            messages.add_message(request, messages.ERROR, 'Поле "Телеграм-юзернейм" пустое, менеджер не создан!')
        super(BotUserAdmin, self).save_model(request, obj, form, change)


    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.botusergroup_set.all()])
    display_groups.short_description = 'Groups'


class BotUserGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    filter_horizontal = ('members',)  # Добавляем это поле

    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('участники', is_stacked=False)}
    }

admin.site.register(BotUserGroup, BotUserGroupAdmin)


class ExtendedUserInline(admin.StackedInline):
    model = ExtendedUser
    exclude = ('category', 'product_manager')
    can_delete = False



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'bot_user_info', 'bot_user_id_info', 'bot_user_category')

    def bot_user_info(self, obj):
        return obj.extended_user.bot_user if obj.extended_user else None

    def bot_user_category(self, obj):
        return obj.extended_user.category if obj.extended_user.category else None

    def bot_user_id_info(self, obj):
        try:
            return obj.extended_user.bot_user.user_id if obj.extended_user else None
        except:
            return 'None'

    inlines = [ExtendedUserInline]






admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
