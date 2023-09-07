from django.db import models
from django.contrib.auth.models import User


class StoryNews(models.Model):

    CHOICES = (
        ('news', 'Новость'),
        ('story', 'Актуальное'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Менеджер')
    name = models.CharField(max_length=64, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    approved = models.BooleanField(default=False, verbose_name='Подтверждено')
    sort = models.CharField(max_length=10, choices=CHOICES, verbose_name='Актуальное/Новость')
    position = models.PositiveIntegerField(null=True, blank=True, verbose_name='Номер позиции')

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = self._get_current_user()
            if current_user:
                self.user = current_user
        super(StoryNews, self).save(*args, **kwargs)

    def _get_current_user(self):
        try:
            return self._context_user
        except AttributeError:
            return None

    def get_manager(self):
        try:
            manager = self.user.extended_user.bot_user.name
            return manager
        except:
            return None

    class Meta:
        verbose_name = 'Актуальное/Новость'
        verbose_name_plural = 'Актуальное/Новости'

    def __str__(self):
        return f"{self.sort}: {self.name}"
