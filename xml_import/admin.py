from django.contrib import admin
from .models import XMLImportSettings

@admin.register(XMLImportSettings)
class XMLImportSettingsAdmin(admin.ModelAdmin):
    list_display = ('folder_path', 'file_name')

    def has_add_permission(self, request):
        return False
