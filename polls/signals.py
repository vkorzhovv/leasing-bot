from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Poll, PollMedia
from bot.django_services import send_poll
from asgiref.sync import async_to_sync

@receiver(post_save, sender=PollMedia)
def poll_created(sender, instance, created, **kwargs):
    if created:
        poll = instance.poll
        send_poll_sync = async_to_sync(send_poll)
        # Проверяем, все ли медиа-файлы загружены для данного поста
        total_media_count = poll.mediafiles.count()
        if poll.total_media_count == total_media_count:
            media_paths = list(PollMedia.objects.filter(poll=instance.poll).values_list('absolute_media_path', flat=True))
            if instance.poll.group is not None:
                send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: {instance.poll.group.id}\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
            else:
                send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)


@receiver(post_save, sender=Poll)
def post_edited(sender, created, instance, **kwargs):
    send_poll_sync = async_to_sync(send_poll)
    if not created:
        if instance.id is not None:
            previous = Poll.objects.get(id=instance.id)
            if not (previous.approved == instance.approved and previous.approved==True):
                media_paths = list(Poll.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
                if instance.group is not None:
                    send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                else:
                    send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
