import dicttoxml
from import_export.formats.base_formats import TextFormat, XLSX
import xmltodict
import tablib
from products.models import ProductMedia
from categories.models import Category
from xml_import.models import ImportStatistics


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

    # def export_data(self, dataset, **kwargs):
    #     """
    #     Returns format representation for given dataset.
    #     """
    #     kwargs.setdefault('attr_type', False)
    #     return dicttoxml.dicttoxml(dataset.dict)

    def export_data(self, dataset, **kwargs):
        """
        Returns format representation for given dataset.
        """
        root_tag = 'Ad'
        xml_content = f"<Ads>\n"
        
        for row in dataset.dict:
            product_id = row['id']
            media_urls = ProductMedia.objects.filter(product__id=product_id).values_list('media_url', flat=True)
            xml_content += "\t<" + root_tag + ">\n"
            for key, value in row.items():
                if key != 'id':
                    if key == 'char_id':
                        key = 'id'
                    xml_content += f"\t\t<{key}>{value}</{key}>\n"
            if media_urls:
                urls = '\n'.join([f'\t\t\t<media url="{url}"/>' for url in media_urls])
                xml_content += f"\t\t<media_url>\n{urls}\n"+"\t\t</media_url>\n"
            xml_content += "\t</" + root_tag + ">\n"
        
        xml_content += f"</Ads>"

        return xml_content


    def create_dataset(self, in_stream):
        import pandas as pd
        from io import StringIO, BytesIO
        import openpyxl
        import xml.etree.ElementTree as ET
          # Используем StringIO для чтения строки как файлоподобного объекта

        # Превращаем строку в объект StringIO
        in_stream_as_file = StringIO(in_stream)

        #ImportStatistics.objects.create()




        # Парсинг XML данных
        tree = ET.parse(in_stream_as_file)
        root = tree.getroot()

        # Проход по каждому элементу <Ad>
        for ad in root.findall('.//Ad'):
            photo_url_element = ad.find('photo_url')
            if photo_url_element is not None:
                # Установка нового значения для элемента photo_url
                photo_url_text = photo_url_element.text
                if  'http://avito.it42' in photo_url_text:
                    if photo_url_text.split('/')[-1]=='':
                        photo_url_text = photo_url_text.split('/')[-2]
                    else:
                        photo_url_text = photo_url_text.split('/')[-1]
                    photo_url_text = '/app/media/share_images/'+photo_url_text
                    photo_url_element.text = photo_url_text

            media_urls = []
            # Получение всех URL медиа из элемента <media_url>
            for media_url in ad.findall('.//media_url/media'):
                url = media_url.get('url')
                if 'http://avito.it42' in url:
                    if url.split('/')[-1]=='':
                        url = url.split('/')[-2]
                    else:
                        url = url.split('/')[-1]
                    url = '/app/media/share_images/'+url
                media_urls.append(url)
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

        # for i, value in enumerate(xml_df['id']):
        #     if not str(value).isdigit():  # Проверяем, является ли значение числом
        #         xml_df.at[i, 'id'] = ''  # Если значение не число, заменяем его на пустую строку

        for i, value in enumerate(xml_df['year']):
            if not str(value).isdigit():  # Проверяем, является ли значение числом
                xml_df.at[i, 'year'] = value[:4]  # Если значение не число, заменяем его на пустую строку

        for i, value in enumerate(xml_df['category']):
            if not Category.objects.filter(id=value):  
                xml_df.at[i, 'category'] = ''


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
        dataset.headers = [cell.value if cell.value!='id' else 'char_id' for cell in next(rows)]
        for row in rows:
            row_values = [cell.value for cell in row]
            dataset.append(row_values)
        return dataset



def create_list_from_ordered_dict(data):
    keys_order = ['id', 'brand', 'category', 'category2', 'product_model', 'name', 'price', 'photo_url', 
                  'description', 'kp_url', 'year', 'promotion', 'manufacturer', 'status', 'equipment', 
                  'hide', 'currency', 'species', 'wheels', 'promotion_description', 'position', 'char_id', 'media_url']
    result = [data[key] for key in keys_order if key in data]
    return result

class XLSX2(XLSX):
    def export_data(self, dataset, **kwargs):
        dataset.headers.append("media_url")

        data = tablib.Dataset()
        data.headers = dataset.headers

        for row in dataset.dict:
            product_id = row['id']
            media_urls = ProductMedia.objects.filter(product__id=product_id).values_list('media_url', flat=True)
            media_url_value = ','.join(media_urls)
            row['media_url'] = media_url_value
            data.append(create_list_from_ordered_dict(row))



        kwargs.pop("escape_output", None)
        if kwargs.pop("escape_html", None):
            self._escape_html(dataset)
        if kwargs.pop("escape_formulae", None):
            self._escape_formulae(dataset)

        return data.export(self.get_title(), **kwargs)