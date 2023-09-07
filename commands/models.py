from django.db import models
from ckeditor.fields import RichTextField

class Command(models.Model):
    key = models.CharField(max_length=64, verbose_name='Ключ')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    text = RichTextField(blank=True, null=True, verbose_name='Текст')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фотография')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')


    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"Сообщение: {self.key}"
