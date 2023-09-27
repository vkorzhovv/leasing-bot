from django.contrib import admin
from .models import Product, Equipment, ProductMedia
from django.core.files import File
import requests
from django.utils.html import mark_safe
import io
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.formats.base_formats import DEFAULT_FORMATS
from products.formats import XML
from import_export import resources





class PostMediaInline(admin.StackedInline):
    model = ProductMedia
    extra = 1  # Количество дополнительных полей для добавления
    readonly_fields = ('absolute_media_path', 'image_preview')




class ProductResource(resources.ModelResource):

    def skip_row(self, instance, original, row, import_validation_errors=None):
        # Проверяем, если у экземпляра пустое поле category
        if not instance.category:
            return True  # Если пусто, игнорируем эту строку
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'photo', 'kp')  # Замените field1, field2 и field3 на реальные имена полей, которые вы хотите исключить




@admin.register(Product)
class BotUserAdmin(ImportExportModelAdmin):

    def image_tag(self, obj):
        if obj.photo:
            return mark_safe('<img src="%s" width="85" height="75" />' % obj.photo.url)

    image_tag.short_description = 'Фото-превью'


    resource_class = ProductResource
    formats = DEFAULT_FORMATS + [XML]
    list_display = ('image_tag', 'id', 'brand', 'product_model', 'name', 'category', 'category2', 'price', 'year', 'promotion', 'hide', 'created_at', 'updated_at', 'position')
    list_filter = ('brand', 'category', 'product_model', 'name', 'price', 'description', 'year', 'promotion', 'manufacturer', 'status', 'equipment', 'created_at', 'updated_at', 'hide', 'currency', 'promotion_description')
    search_fields = ('brand', 'product_model', 'name')
    ordering = ('-created_at',)
    list_editable = ('promotion',)
    list_display_links = ('id', 'brand', 'product_model')
    inlines = [PostMediaInline]
    readonly_fields = ['image_tag']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
