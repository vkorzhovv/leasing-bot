from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Poll, PollMedia
from bot.django_services import send_poll
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger('django')

@receiver(post_save, sender=PollMedia)
def poll_created(sender, instance, created, **kwargs):
    if created:
        logger.info("PollMedia has been created: %s", instance.poll.title)
        poll = instance.poll
        send_poll_sync = async_to_sync(send_poll)
        # Проверяем, все ли медиа-файлы загружены для данного поста
        total_media_count = poll.mediafiles.count()
        if poll.total_media_count == total_media_count:
            logger.info("poll.total_media_count == total_media_count: %s", instance.poll.title)
            media_paths = list(PollMedia.objects.filter(poll=instance.poll).values_list('absolute_media_path', flat=True))
            if instance.poll.group is not None:
                send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: {instance.poll.group.id}\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
                logger.info("Poll with group has been sent to the admin: %s", instance.poll.title)
            else:
                send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
                logger.info("Poll without group has been sent to the admin: %s", instance.poll.title)
        else:
            logger.info("ERROR: poll.total_media_count != total_media_count: %s", instance.poll.title)


@receiver(post_delete, sender=PollMedia)
def poll_deleted(sender, instance, **kwargs):
    logger.info("PollMedia has been deleted")
    poll = instance.poll
    send_poll_sync = async_to_sync(send_poll)
    # Проверяем, все ли медиа-файлы загружены для данного поста
    total_media_count = poll.mediafiles.count()
    if poll.total_media_count == total_media_count:
        logger.info("delete media: poll.total_media_count == total_media_count: %s", instance.poll.title)
        media_paths = list(PollMedia.objects.filter(poll=instance.poll).values_list('absolute_media_path', flat=True))
        if instance.poll.group is not None:
            send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: {instance.poll.group.id}\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
            logger.info("delete media: Poll with group has been sent to the admin: %s", instance.poll.title)
        else:
            send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
            logger.info("delete media: Poll without group has been sent to the admin: %s", instance.poll.title)
    else:
        logger.info("ERROR: poll.total_media_count != total_media_count: %s", instance.poll.title)


@receiver(pre_save, sender=Poll)
def post_edited(sender, instance, **kwargs):
    send_poll_sync = async_to_sync(send_poll)
    # if not created:
    logger.info("Poll has been changed: %s", instance.title)
    if instance.id is not None:
        print('edited')
        previous = Poll.objects.get(id=instance.id)
        if instance.approved!=True and previous.total_media_count==instance.total_media_count:
            logger.info("not (previous.approved == instance.approved and previous.approved==True) and previous.total_media_count==instance.total_media_count==True: %s", instance.title)
            media_paths = list(Poll.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
            if instance.group is not None:
                send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                logger.info("edit: Poll with group has been sent to the admin again: %s", instance.title)
            else:
                send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                logger.info("edit: Poll without group has been sent to the admin again: %s", instance.title)


@receiver(post_save, sender=Poll)
def post_without_media_created(sender, created, instance, **kwargs):
    send_poll_sync = async_to_sync(send_poll)
    if created:
        if instance.total_media_count==0:
            if instance.group is not None:
                send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
                logger.info("edit: Poll with group has been sent to the admin again: %s", instance.title)
            else:
                send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
                logger.info("edit: Poll without group has been sent to the admin again: %s", instance.title)
