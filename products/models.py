from django.db import models
from categories.models import Category
import requests
from urllib.parse import urlencode
from django.core.files import File
import io


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

    SPECIES_CHOICES = (
        ('truck', 'Грузовик'),
        ('pickup', 'Пикап'),
        ('dump', 'Самосвал'),
    )

    brand = models.CharField(max_length=128, null=True, blank=True, verbose_name='Марка')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name = 'products', verbose_name='Категория')
    category2 = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name = 'products2', verbose_name='Категория2')
    product_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='Модель')
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True, verbose_name='Стоимость')
    photo = models.ImageField(upload_to='images', blank=True, verbose_name='Фотография')
    photo_url = models.CharField(max_length=128, null=True, blank=True, verbose_name='Адрес для яндекс-картинки')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Год выпуска')
    promotion = models.BooleanField(default=False, verbose_name='Акция')
    manufacturer = models.CharField(max_length=128, null=True, blank=True, verbose_name='Страна производителя')
    status = models.CharField(max_length=10, choices=CHOICES, null=True, blank=True, verbose_name='Статус')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name='Комплектация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True, null=True, default='RUB', verbose_name='Валюта')
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES, blank=True, null=True, verbose_name='Вид техники')
    wheels = models.CharField(max_length=64, blank=True, null=True, verbose_name='Колёсная формула')
    promotion_description = models.TextField(null=True, blank=True, verbose_name='Описание акции')
    position = models.PositiveIntegerField(null=True, blank=True, verbose_name='Номер позиции в категории')

    def save(self, *args, **kwargs):

        if self.photo_url:
            base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
            public_key = self.photo_url

            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']

            download_response = requests.get(download_url)
            file_content = download_response.content

            file_name = self.photo_url.split('/')[-1]
            temp_file = File(io.BytesIO(file_content), name=file_name+'.jpg')
            self.photo = temp_file

        super().save(*args, **kwargs)



    def __str__(self):
        if self.name!=None:
            return self.name
        return 'Без названия'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
