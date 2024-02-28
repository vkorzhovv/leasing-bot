import dicttoxml
from import_export.formats.base_formats import TextFormat
import xmltodict
import tablib


class XML(TextFormat):
    def get_title(self):
        return 'xml'

    def is_binary(self):
        """
        Returns if this format is binary.
        """
        return False

    def get_extension(self):
        """
        Returns extension for this format files.
        """
        return ".xml"

    def get_content_type(self):
        return 'application/xml'

    def can_import(self):
        return True

    def can_export(self):
        return True

    def export_data(self, dataset, **kwargs):
        """
        Returns format representation for given dataset.
        """
        kwargs.setdefault('attr_type', False)
        return dicttoxml.dicttoxml(dataset.dict)


    def create_dataset(self, in_stream):
        import pandas as pd
        from io import StringIO, BytesIO
        import openpyxl
        import xml.etree.ElementTree as ET
          # Используем StringIO для чтения строки как файлоподобного объекта

        # Превращаем строку в объект StringIO
        in_stream_as_file = StringIO(in_stream)




        # Парсинг XML данных
        tree = ET.parse(in_stream_as_file)
        root = tree.getroot()

        # Проход по каждому элементу <Ad>
        for ad in root.findall('.//Ad'):
            media_urls = []
            # Получение всех URL медиа из элемента <media_url>
            for media_url in ad.findall('.//media_url/media'):
                media_urls.append(media_url.get('url'))
                # Удаление дочерних элементов <media>
                ad.find('.//media_url').remove(media_url)
            # Объединение URL медиа в одну строку через пробел
            combined_media_url = ','.join(media_urls)
            # Присваивание объединенной строки в качестве текста элемента <media_url>
            ad.find('.//media_url').text = combined_media_url

        # Преобразование XML обратно в строку
        xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')




        # Читаем XML данные из строки
        # xml_df = pd.read_xml(in_stream_as_file)
        xml_df = pd.read_xml(StringIO(xml_string))

        for i, value in enumerate(xml_df['id']):
            if not str(value).isdigit():  # Проверяем, является ли значение числом
                xml_df.at[i, 'id'] = ''  # Если значение не число, заменяем его на пустую строку

        for i, value in enumerate(xml_df['year']):
            if not str(value).isdigit():  # Проверяем, является ли значение числом
                xml_df.at[i, 'year'] = value[:4]  # Если значение не число, заменяем его на пустую строку


        # Удаляем столбцы <created_at>, <updated_at>, <year>
        columns_to_drop = ['created_at', 'updated_at']
        xml_df = xml_df.drop(columns=columns_to_drop, errors='ignore')

        # Остальная часть кода остается неизменной
        excel_buffer = BytesIO()
        xml_df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        xlsx_book = openpyxl.load_workbook(excel_buffer)
        dataset = tablib.Dataset()
        sheet = xlsx_book.active
        rows = sheet.rows
        dataset.headers = [cell.value for cell in next(rows)]
        for row in rows:
            row_values = [cell.value for cell in row]
            dataset.append(row_values)
        return dataset
