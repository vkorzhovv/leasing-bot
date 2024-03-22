from django.contrib import admin
from .models import Product, Equipment, ProductMedia
from django.core.files import File
import requests
from django.utils.html import mark_safe
import io
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.formats.base_formats import DEFAULT_FORMATS
from products.formats import XML, XLSX2, create_list_from_ordered_dict
from import_export import resources, fields, widgets
import openpyxl
from xml_import.models import ImportStatistics
from categories.models import Category




class ProductMediaResource(resources.ModelResource):

    def skip_row(self, instance, original, row, import_validation_errors=None):
        # Проверяем, если у экземпляра пустое поле category
        if not instance.media_url:
            return True  # Если пусто, игнорируем эту строку
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

    class Meta:
        model = ProductMedia
        exclude = ('media', 'absolute_media_path')  # Замените field1, field2 и field3 на реальные имена полей, которые вы хотите исключить




@admin.register(ProductMedia)
class ProductMediaAdmin(ImportExportModelAdmin):
    resource_class = ProductMediaResource
    list_display = ('id', 'media', 'media_url', 'absolute_media_path')







class PostMediaInline(admin.StackedInline):
    model = ProductMedia
    extra = 1  # Количество дополнительных полей для добавления
    readonly_fields = ('absolute_media_path', 'image_preview')




class ProductResource(resources.ModelResource):
    def __init__(self, **kwargs):
        super(ProductResource, self).__init__(**kwargs)
        self.media_urls = []
        self.statistics = ImportStatistics.objects.first()

    def before_import_row(self, row, row_number=None, **kwargs):
        print(row['char_id'])
        if 'media_url' in row:
            if row['media_url']!=None:
                for url in row['media_url'].split(','):
                    self.media_urls.append(url)

    def after_save_instance(self, instance, using_transactions, dry_run):
        if Product.objects.filter(id=instance.id).exists():
            ProductMedia.objects.filter(product=instance).delete()
            for media_url in self.media_urls:
                try:
                    ProductMedia(media_url=media_url, product=instance).save()
                except:
                    None
        self.media_urls = []

    def skip_row(self, instance, original, row, import_validation_errors=None):
        # Проверяем, если у экземпляра пустое поле category
        # print('ROW$$$$$$$$$$$$$$$$$$$$$$$$$$:', create_list_from_ordered_dict(row))
        if (not instance.category) or (import_validation_errors):
            self.statistics.skipped_info+=f'Артикул: {instance.char_id}, Название: {instance.name}, Марка: {instance.brand}\n'
            self.statistics.skipped+=1
            self.statistics.save()
            return True  # Если пусто, игнорируем эту строку
        if Product.objects.filter(id=instance.id):
            self.statistics.updated+=1
            self.statistics.save()
        else:
            self.statistics.imported+=1
            self.statistics.save()

        if import_validation_errors:
          return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)

    class Meta:
        model = Product
        import_id_fields = ("char_id",)
        exclude = ('created_at', 'updated_at', 'photo', 'kp')  # Замените field1, field2 и field3 на реальные имена полей, которые вы хотите исключить


@admin.register(Product)
class BotUserAdmin(ImportExportModelAdmin):

    def image_tag(self, obj):
        if obj.photo:
            return mark_safe('<img src="%s" width="85" height="75" />' % obj.photo.url)

    image_tag.short_description = 'Фото-превью'


    resource_class = ProductResource
    formats = DEFAULT_FORMATS + [XML] + [XLSX2]
    formats.pop(2)
    list_display = ('image_tag', 'id', 'char_id', 'brand', 'product_model', 'name', 'category', 'category2', 'price', 'year', 'promotion', 'hide', 'created_at', 'updated_at', 'position')
    list_filter = ('brand', 'category', 'product_model', 'name', 'price', 'description', 'year', 'promotion', 'manufacturer', 'status', 'equipment', 'created_at', 'updated_at', 'hide', 'currency', 'promotion_description')
    search_fields = ('brand', 'product_model', 'name')
    ordering = ('-created_at',)
    list_editable = ('promotion',)
    list_display_links = ('id', 'brand', 'product_model')
    inlines = [PostMediaInline]
    readonly_fields = ['char_id', 'image_tag']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')






# def import_data_from_xml(folder_path, file_name):
#     from .formats import XML
#     # Полный путь к XML файлу
#     xml_file_path = f"{folder_path}/{file_name}"

#     # Создаем экземпляр ресурса
#     resource = ProductResource()

    
#     xml_formatter  = XML()
#     with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
#         # Создаем dataset из XML данных
#         data = xml_formatter.create_dataset(xml_file.read())

#     # Импортируем данные из XML файла
#     dataset = resource.import_data(dataset=data, raise_errors=True)
#     # Возвращаем результат импорта
#     return dataset


# import_data_from_xml(r'\\LAPTOP-2554OM7H\Users\hp\Desktop\green card', 'data.xml')