from django.urls import path
from .views import create_xml_import_settings, make_xml_import

urlpatterns = [
    path('create_xml_import_settings/', create_xml_import_settings, name='create_xml_import_settings'),
    path('make_xml_import/', make_xml_import)
]
