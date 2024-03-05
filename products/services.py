import re
from import_export.resources import modelresource_factory
import logging
from src.celery import app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='xml-import.log')

def remove_special_characters(input_string):
    # Используем регулярное выражение для удаления всех символов, кроме букв и цифр
    result = re.sub(r'[^a-zA-Z0-9а-яА-Я\s]', '', input_string)
    return result.replace(' ', '_')

# @app.task(bind=True)
def import_data_from_xml():
    from .admin import ProductResource
    from xml_import.models import XMLImportSettings
    from .formats import XML

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


# import_data_from_xml(r'\\LAPTOP-2554OM7H\Users\hp\Desktop\green card', 'data.xml')