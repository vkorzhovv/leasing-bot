from django.db import models

class XMLImportSettings(models.Model):
    folder_path = models.CharField(max_length=255, verbose_name='Путь к папке')
    file_name = models.CharField(max_length=255, verbose_name='Название файла')
    # first_import_time = models.TimeField(verbose_name='Время первого импорта')
    # second_import_time = models.TimeField(verbose_name='Время второго импорта')


    def __str__(self):
        return f'{self.folder_path} - {self.file_name}'


    class Meta:
    	verbose_name = 'Настройки XML импорта'
    	verbose_name_plural = 'Настройки XML импорта'


class ImportStatistics(models.Model):
    imported = models.IntegerField('Импортировано товаров', default=0)
    skipped = models.IntegerField('Пропущено товаров', default=0)
    updated = models.IntegerField('Обновлено товаров', default=0)
    skipped_info = models.TextField('Информация о пропущенных товарах', default='')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статистика XML импорта'
        verbose_name_plural = 'Статистика XML импорта'
        ordering = ['-date']