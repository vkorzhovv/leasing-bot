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
        file_name='data.xml',
        first_import_time='12:00:00',
        second_import_time='18:00:00'
    )

    return JsonResponse({'message': 'Экземпляр модели успешно создан'}, status=201)
 	


def make_xml_import(request):
    from products.services import import_data_from_xml

    try:
        import_data_from_xml()
        return JsonResponse({'message': 'Товары успешно импортированы'}, status=201)
    except:
        return JsonResponse({'message': 'Импортировать товары не удалось'}, status=201)



def import_statistics_view(request):
    statistics = ImportStatistics.objects.all()
    return render(request, 'xml_import/import_statistics.html', {'statistics': statistics})
