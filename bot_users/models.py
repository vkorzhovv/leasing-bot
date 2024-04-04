from django.db import models
from django.contrib.auth.models import AbstractUser, User
from categories.models import Category


class BotUser(models.Model):
    name = models.CharField(max_length=128, verbose_name='ФИО')
    company_name = models.CharField(max_length=128, verbose_name='Название компании')
    phone = models.CharField(max_length=20, verbose_name='Номер')
    photo = models.ImageField(upload_to='images', blank=True, verbose_name='Фотография')
    activated = models.BooleanField(default=False, verbose_name='Подтверждён')
    user_id = models.CharField(max_length=128, unique=True, verbose_name='Телеграм-ID', default='Admin')
    username = models.CharField(max_length=128, blank=True, null=True, verbose_name='Телеграм-юзернейм')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    last_interaction = models.DateTimeField(null=True, blank=True, verbose_name='Последняя активность')
    manager = models.BooleanField(default=False, verbose_name='Менеджер')
    city = models.CharField(max_length=64, blank=True, null=True, verbose_name='Город')
    last_viewed_category_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='ID последней просмотренной категории')

    def __str__(self):
        return f'{self.name}({self.company_name})'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

class BotUserGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    members = models.ManyToManyField(BotUser, verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменён')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа пользователей бота'
        verbose_name_plural = 'Группы пользователей бота'


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_user')
    bot_user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Телеграм-пользователь менеджера')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория менеджера')
    product_manager = models.BooleanField("Менеджер по поиску товаров", default=False)