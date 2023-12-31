from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Poll, PollMedia
from bot.django_services import send_poll, delete_post_message
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger('django')
poll_message_id = {}

# @receiver(post_save, sender=PollMedia)
# def poll_created(sender, instance, created, **kwargs):
#     print('pollmedia post_save')
#     if created:
#         logger.info("PollMedia has been created: %s", instance.poll.title)
#         poll = instance.poll
#         send_poll_sync = async_to_sync(send_poll)
#         # Проверяем, все ли медиа-файлы загружены для данного поста
#         total_media_count = poll.mediafiles.count()
#         if poll.total_media_count == total_media_count:
#             logger.info("poll.total_media_count == total_media_count: %s", instance.poll.title)
#             media_paths = list(PollMedia.objects.filter(poll=instance.poll).values_list('absolute_media_path', flat=True))
#             if instance.poll.group is not None:
#                 send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: {instance.poll.group.id}\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
#                 logger.info("Poll with group has been sent to the admin: %s", instance.poll.title)
#             else:
#                 send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
#                 logger.info("Poll without group has been sent to the admin: %s", instance.poll.title)
#         else:
#             logger.info("ERROR: poll.total_media_count != total_media_count: %s", instance.poll.title)


# @receiver(post_delete, sender=PollMedia)
# def poll_deleted(sender, instance, **kwargs):
#     print('pollmedia post_delete')
#     logger.info("PollMedia has been deleted")
#     poll = instance.poll
#     send_poll_sync = async_to_sync(send_poll)
#     # Проверяем, все ли медиа-файлы загружены для данного поста
#     total_media_count = poll.mediafiles.count()
#     if poll.total_media_count == total_media_count:
#         logger.info("delete media: poll.total_media_count == total_media_count: %s", instance.poll.title)
#         media_paths = list(PollMedia.objects.filter(poll=instance.poll).values_list('absolute_media_path', flat=True))
#         if instance.poll.group is not None:
#             send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: {instance.poll.group.id}\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
#             logger.info("delete media: Poll with group has been sent to the admin: %s", instance.poll.title)
#         else:
#             send_poll_sync(f'ID опроса: {instance.poll.id}\nЗаголовок опроса: {instance.poll.title}\nВарианты ответа: {instance.poll.options}\nПравильный ответ: {instance.poll.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.poll.user.extended_user.bot_user.user_id} ({instance.poll.user.extended_user.user.username}|запланировано на {instance.poll.scheduled_time})', media_paths)
#             logger.info("delete media: Poll without group has been sent to the admin: %s", instance.poll.title)
#     else:
#         logger.info("ERROR: poll.total_media_count != total_media_count: %s", instance.poll.title)


# @receiver(pre_save, sender=Poll)
# def post_edited(sender, instance, **kwargs):
#     print('poll pre_save')
#     send_poll_sync = async_to_sync(send_poll)
#     # if not created:
#     logger.info("Poll has been changed: %s", instance.title)
#     if instance.id is not None:
#         previous = Poll.objects.get(id=instance.id)
#         if instance.approved!=True and previous.total_media_count==instance.total_media_count:
#             logger.info("not (previous.approved == instance.approved and previous.approved==True) and previous.total_media_count==instance.total_media_count==True: %s", instance.title)
#             media_paths = list(Poll.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
#             if instance.group is not None:
#                 send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
#                 logger.info("edit: Poll with group has been sent to the admin again: %s", instance.title)
#             else:
#                 send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
#                 logger.info("edit: Poll without group has been sent to the admin again: %s", instance.title)


# @receiver(post_save, sender=Poll)
# def post_without_media_created(sender, created, instance, **kwargs):
#     print('poll post_save')
#     send_poll_sync = async_to_sync(send_poll)
#     if created:
#         if instance.total_media_count==0:
#             if instance.group is not None:
#                 send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
#                 logger.info("edit: Poll with group has been sent to the admin again: %s", instance.title)
#             else:
#                 send_poll_sync(f'ID опроса: {instance.id}\nЗаголовок опроса: {instance.title}\nВарианты ответа: {instance.options}\nПравильный ответ: {instance.correct_answer}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
#                 logger.info("edit: Poll without group has been sent to the admin again: %s", instance.title)


@receiver(post_save, sender=Poll)
def post_without_media_created(sender, created, instance, **kwargs):
    global poll_message_id
    poll_id = instance.id
    if not created:
        send_poll_sync = async_to_sync(send_poll)
        delete_poll_message_sync = async_to_sync(delete_post_message)
        try:
            if instance.approved==False:
                poll_message = poll_message_id.get(poll_id, [])
                for message in poll_message[1:]:
                    delete_poll_message_sync(user_id=poll_message[0], message_id=message)
                print([media.absolute_media_path for media in instance.mediafiles.all()])
                if instance.user.extended_user.bot_user.username:
                    manager = '@'+instance.user.extended_user.bot_user.username
                else:
                    manager = None

                if instance.group:
                    group = instance.group.name
                else:
                    group = None

    

                poll_message_id[poll_id] = send_poll_sync(instance.id, [(option.id, option.option) for option in instance.options.all()], instance.title, instance.scheduled_time, manager, group, [media.absolute_media_path for media in instance.mediafiles.all()])
        except:
            pass
