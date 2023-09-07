from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import os

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Менеджер')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время рассылки")
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    options = models.TextField(verbose_name='Варианты ответа')
    correct_answer = models.PositiveIntegerField(blank=True, null=True, verbose_name='Правильный ответ(если пусто, то без правильных ответов)')
    approved = models.BooleanField(default=False, verbose_name='Подтверждён')
    total_media_count = models.PositiveIntegerField(default=0, verbose_name='Сколько фотографий загрузите?')
    group = models.ForeignKey('bot_users.BotUserGroup', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Группа пользователей бота')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Создано')


    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = self._get_current_user()
            if current_user:
                self.user = current_user
        super(Poll, self).save(*args, **kwargs)

    def _get_current_user(self):
        try:
            return self._context_user
        except AttributeError:
            return None

    def __str__(self):
        return f"Опрос от {self.user.username}"

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'



class PollMedia(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='mediafiles', verbose_name='Опрос')
    media = models.FileField(upload_to='poll_media/', blank=True, verbose_name='Медиа')
    absolute_media_path = models.CharField(max_length=255, blank=True, verbose_name='Абсолютный путь до медиа')

    def save(self, *args, **kwargs):
        self.absolute_media_path = self.get_absolute_media_path()
        return super().save(*args, **kwargs)

    def get_absolute_media_path(self):
        media_filename = os.path.basename(self.media.path)
        return os.path.join(settings.BASE_DIR, 'media', 'poll_media', media_filename)


    class Meta:
        verbose_name = 'Медиа'
        verbose_name_plural = 'Медиа'

    def __str__(self):
        return f"Объект ({self.id})"
