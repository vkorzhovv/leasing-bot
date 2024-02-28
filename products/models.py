from django.db import models
from categories.models import Category
import requests
from urllib.parse import urlencode
from django.core.files import File
import io
from django.conf import settings
import os
from django.utils.safestring import mark_safe
from urllib.parse import urlparse, unquote
from .services import remove_special_characters
from django_resized import ResizedImageField
from PIL import Image
import cv2
import shutil
from django.conf import settings

class Equipment(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комплектация'
        verbose_name_plural = 'Комплектации'


class Product(models.Model):

    CHOICES = (
        ('instock', 'В наличии'),
        ('supply', 'Поставка'),
    )

    CURRENCY_CHOICES = (
        ('RUB', 'rub'),
        ('USD', 'usd'),
        ('EUR', 'eur'),
        ('CNY', 'cny'),
    )

    # SPECIES_CHOICES = (
    #     ('truck', 'Грузовик'),
    #     ('pickup', 'Пикап'),
    #     ('dump', 'Самосвал'),
    # )

    brand = models.CharField(max_length=128, null=True, blank=True, verbose_name='Марка')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name = 'products', verbose_name='Категория')
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name = 'products2', verbose_name='Категория2')
    product_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='Модель')
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True, verbose_name='Стоимость')
    photo = models.ImageField(upload_to='images', blank=True, verbose_name='Фотография')
    photo_url = models.CharField(max_length=128, null=True, blank=True, verbose_name='Адрес для яндекс-картинки')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    kp = models.FileField('КП', upload_to='kp/', blank=True, null=True)
    kp_url = models.CharField(max_length=128, null=True, blank=True, verbose_name='Адрес для яндекс-файла')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Год выпуска')
    promotion = models.BooleanField(default=False, verbose_name='Акция')
    manufacturer = models.CharField(max_length=128, null=True, blank=True, verbose_name='Страна производителя')
    status = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True, verbose_name='Статус')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name='Комплектация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True, null=True, default='RUB', verbose_name='Валюта')
    # species = models.CharField(max_length=20, choices=SPECIES_CHOICES, blank=True, null=True, verbose_name='Вид техники')
    species = models.CharField(max_length=64, blank=True, null=True, verbose_name='Вид техники')
    wheels = models.CharField(max_length=64, blank=True, null=True, verbose_name='Колёсная формула')
    promotion_description = models.TextField(null=True, blank=True, verbose_name='Описание акции')
    position = models.PositiveIntegerField(null=True, blank=True, verbose_name='Номер позиции в категории')

    def save(self, *args, **kwargs):

        if self.photo_url:
            if 'yandex' in self.photo_url:
                base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
                public_key = self.photo_url

                final_url = base_url + urlencode(dict(public_key=public_key))
                response = requests.get(final_url)
                download_url = response.json()['href']
                parsed_url = urlparse(download_url)
                filename = unquote(parsed_url.query.split("&filename=")[1].split("&")[0])
                splitted = filename.split('.')
                extension = splitted[-1]
                name = '.'.join(splitted[0:-1])
                filename = remove_special_characters(name)
                filename = filename+'.'+extension


            elif self.photo_url.startswith('http'):
                download_url = self.photo_url
                parsed_url = urlparse(download_url)
                filename = parsed_url.path.split('/')[-1]
                extension = filename.split('.')[-1]


            else:
                download_url = self.photo_url # например: //SHARE/All/Асеева Алина/Телеграм бот/1_80cc3040-77ce-4f1e-bf08-d83dc4e7ce84.jpeg
                filename = os.path.basename(download_url)
                extension = download_url.split('.')[-1]

                destination_path = "media\\product_media"  # Укажите путь куда скопировать файл

                shutil.copy(download_url, os.path.join(destination_path, filename))



            if 'yandex' in self.photo_url or self.photo_url.startswith('http'):
                download_response = requests.get(download_url)
                file_content = download_response.content


                temp_file = File(io.BytesIO(file_content), name=filename)
                self.photo = temp_file
                super().save(*args, **kwargs)
            else:
                # with open(os.path.join(destination_path, filename), 'rb') as f:
                #     temp_file = File(f, name=filename)
                #     self.photo = temp_file
                with open(os.path.join(destination_path, filename), 'rb') as f:
                    file_content = f.read()

                    # Создаем временный файл и сохраняем его в модели
                    temp_file = File(io.BytesIO(file_content), name=filename)
                    self.photo = temp_file
                    super().save(*args, **kwargs)



            image = cv2.imread(self.photo.path, cv2.IMREAD_COLOR)
            height, width = image.shape[:2]  
            print(height, width)   


            if height > 1280 or width > 1280:
                # Вычисляем масштаб для изменения размеров с сохранением пропорций
                scale_factor = min(1280 / height, 1280 / width)

                # Рассчитываем новые размеры с сохранением пропорций
                new_height = int(height * scale_factor)
                new_width = int(width * scale_factor)

                print(new_width, new_height)
                # Изменяем размер изображения до 1280x640
                resized_image = cv2.resize(image, (new_width, new_height))

                # Сохраняем измененное изображение во временный буфер
                _, buffer = cv2.imencode('.' + extension, resized_image)
                temp_file = File(io.BytesIO(buffer.tobytes()), name=filename)
                self.photo = temp_file 

            elif not (height > 1280 or width > 1280):
                self.photo = temp_file



        if self.kp_url:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = self.kp_url

            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            parsed_url = urlparse(download_url)
            filename = unquote(parsed_url.query.split("&filename=")[1].split("&")[0])
            download_response = requests.get(download_url)
            file_content = download_response.ContentTypes

            temp_file = File(io.BytesIO(file_content), name=filename)
            self.kp = temp_file

        super().save(*args, **kwargs)


    def __str__(self):
        if self.name!=None:
            return self.name
        return 'Без названия'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'



class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles', verbose_name='Товар')
    media = models.FileField(upload_to='product_media/', blank=True, null=True, verbose_name='Доп. фотки')
    media_url = models.CharField(max_length=128, null=True, blank=True, verbose_name='Адрес для яндекс-картинки')
    absolute_media_path = models.CharField(max_length=255, blank=True, verbose_name='Абсолютный путь до медиа')

    def save(self, *args, **kwargs):
        if self.media_url:
            if 'yandex' in self.media_url:
                base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
                public_key = self.media_url

                final_url = base_url + urlencode(dict(public_key=public_key))
                response = requests.get(final_url)
                download_url = response.json()['href']
                parsed_url = urlparse(download_url)
                filename = unquote(parsed_url.query.split("&filename=")[1].split("&")[0])
                splitted = filename.split('.')
                extension = splitted[-1]
                name = '.'.join(splitted[0:-1])
                filename = remove_special_characters(name)
                filename = filename+'.'+extension


            elif self.media_url.startswith('http'):
                download_url = self.media_url
                parsed_url = urlparse(download_url)
                filename = parsed_url.path.split('/')[-1]
                extension = filename.split('.')[-1]


            else:
                download_url = self.media_url # например: //SHARE/All/Асеева Алина/Телеграм бот/1_80cc3040-77ce-4f1e-bf08-d83dc4e7ce84.jpeg
                filename = os.path.basename(download_url)
                extension = download_url.split('.')[-1]

                destination_path = "media\\product_media"  # Укажите путь куда скопировать файл

                shutil.copy(download_url, os.path.join(destination_path, filename))



            if 'yandex' in self.media_url or self.media_url.startswith('http'):
                download_response = requests.get(download_url)
                file_content = download_response.content


                temp_file = File(io.BytesIO(file_content), name=filename)
                self.media = temp_file
                super().save(*args, **kwargs)
            else:
                # with open(os.path.join(destination_path, filename), 'rb') as f:
                #     temp_file = File(f, name=filename)
                #     self.photo = temp_file
                with open(os.path.join(destination_path, filename), 'rb') as f:
                    file_content = f.read()

                    # Создаем временный файл и сохраняем его в модели
                    temp_file = File(io.BytesIO(file_content), name=filename)
                    self.media = temp_file
                    super().save(*args, **kwargs)

        if self.media:
            self.absolute_media_path = self.get_absolute_media_path()
        return super().save(*args, **kwargs)

    def get_absolute_media_path(self):
        media_filename = os.path.basename(self.media.path)
        return os.path.join(settings.BASE_DIR, 'media', 'product_media', media_filename)


    def image_preview(self):
        if self.media:
            return mark_safe('<img src="%s" width="170" height="150" />' % self.media.url)
        else:
            return 'Нет фотки'


    class Meta:
        verbose_name = 'Дополнительные фото'
        verbose_name_plural = 'Дополнительные фото'

    def __str__(self):
        return f"Объект ({self.id})"
