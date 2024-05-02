from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import XMLImportSettings, ImportStatistics
from django.conf import settings
from django.shortcuts import render

@csrf_exempt
def create_xml_import_settings(request):
    # Проверяем, существует ли уже экземпляр модели
    if XMLImportSettings.objects.exists():
        return JsonResponse({'message': 'Экземпляр модели уже существует'}, status=400)
    
    # Создаем новый экземпляр модели с заданными значениями
    xml_import_settings = XMLImportSettings.objects.create(
        folder_path=settings.XML_FOLDER_PATH,
        file_name='data.xml'
    )

    return JsonResponse({'message': 'Экземпляр модели успешно создан'}, status=201)
 	


def make_xml_import(request):
    # from products.services import import_data_from_xml
    from products.tasks import import_data_from_xml

    try:
        # import_data_from_xml()
        import_data_from_xml.delay()
        return JsonResponse({'message': 'Поставили в очередь на импорт'}, status=201)
    except Exception as e:
        return JsonResponse({'message': f'Импортировать товары не удалось: {str(e)}'}, status=500)


def import_statistics_view(request):
    statistics = ImportStatistics.objects.all()
    return render(request, 'xml_import/import_statistics.html', {'statistics': statistics})
