from celery import shared_task
import logging
import sys


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger('').addHandler(console_handler)


@shared_task
def import_data_from_xml(*args):
    from .admin import ProductResource
    from xml_import.models import XMLImportSettings, ImportStatistics
    from .formats import XML


    ImportStatistics.objects.create()

    xml_settings = XMLImportSettings.objects.all().first()
    logging.info(f'xml_settings:{xml_settings}')


    folder_path = xml_settings.folder_path
    logging.info(f'folder_path:{folder_path}')
    file_name = xml_settings.file_name
    logging.info(f'file_name:{file_name}')

    # Полный путь к XML файлу
    xml_file_path = f"{folder_path}/{file_name}"
    logging.info(f'xml_file_path:{xml_file_path}')



    # Создаем экземпляр ресурса
    resource = ProductResource()
    logging.info(f'resource:{resource}')

    
    xml_formatter  = XML()
    logging.info(f'xml_formatter:{xml_formatter}')
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        # Создаем dataset из XML данных
        data = xml_formatter.create_dataset(xml_file.read())
        logging.info(f'data:{data}')

    # Импортируем данные из XML файла
    dataset = resource.import_data(dataset=data, raise_errors=True)
    logging.info(f'dataset:{dataset}')

    # Возвращаем результат импорта
    return dataset
