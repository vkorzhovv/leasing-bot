from django.urls import path
from .views import create_xml_import_settings, make_xml_import, import_statistics_view

urlpatterns = [
    path('create_xml_import_settings/', create_xml_import_settings, name='create_xml_import_settings'),
    path('make_xml_import/', make_xml_import),
    path('import_statistics/', import_statistics_view, name='import_statistics'),
]
