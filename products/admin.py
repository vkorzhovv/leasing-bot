from django.contrib import admin
from .models import Product, Equipment
from django.core.files import File
import requests
import io
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin


@admin.register(Product)
class BotUserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'brand', 'product_model', 'name', 'category', 'category2', 'price', 'year', 'promotion', 'hide', 'created_at', 'updated_at', 'position')
    list_filter = ('brand', 'category', 'product_model', 'name', 'price', 'description', 'year', 'promotion', 'manufacturer', 'status', 'equipment', 'created_at', 'updated_at', 'hide', 'currency', 'promotion_description')
    search_fields = ('brand', 'product_model', 'name')
    ordering = ('-created_at',)
    list_editable = ('promotion',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
