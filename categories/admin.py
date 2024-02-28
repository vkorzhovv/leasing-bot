from django.contrib import admin
from .models import Category


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_filter = ('name', 'parent')
#     search_fields = ('name', 'parent')
#     list_display = ('id', 'name', 'parent', 'position')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'position')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('parent',)
    exclude = ('last_position', )


    # def indented_name(self, obj):
    #     lst = obj.get_level()[0]
    #     # Создание отступов для визуального отображения иерархии
    #     return f"{'>'.join(reversed(lst))}>{obj.name}"

    # indented_name.short_description = 'Название'

admin.site.register(Category, CategoryAdmin)
