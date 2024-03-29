from django import forms
from django.contrib import admin
from .models import Category


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_filter = ('name', 'parent')
#     search_fields = ('name', 'parent')
#     list_display = ('id', 'name', 'parent', 'position')


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []  # Здесь могут быть исключены другие поля, если это необходимо

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('id', 'name', 'parent', 'position', 'bot_user_category')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('parent',)
    exclude = ('last_position', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        if obj:  # Проверяем, существует ли объект для редактирования
            if obj.children.exists():  # Проверяем, имеет ли категория дочерние элементы
                # Если да, скрываем поле 'users'
                form.base_fields.pop('users', None)
        return form

    def bot_user_category(self, obj):
        print(self, obj)
        text = ""
        for item in obj.users.all():
            text += f"{item.username} "
        return text if text else "-"


    # def indented_name(self, obj):
    #     lst = obj.get_level()[0]
    #     # Создание отступов для визуального отображения иерархии
    #     return f"{'>'.join(reversed(lst))}>{obj.name}"

    # indented_name.short_description = 'Название'

admin.site.register(Category, CategoryAdmin)
