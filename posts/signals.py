from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Post, PostMedia
from bot.django_services import send_post, get_post_path
from asgiref.sync import async_to_sync
import logging

logger = logging.getLogger('django')

# @receiver(post_save, sender=PostMedia)
# def post_created(sender, instance, created, **kwargs):
#     if created:
#         logger.info("PostMedia has been created: %s", instance.post.id)
#         post = instance.post
#         send_post_sync = async_to_sync(send_post)
#         # Проверяем, все ли медиа-файлы загружены для данного поста
#         total_media_count = post.mediafiles.count()
#         if post.total_media_count == total_media_count:
#             logger.info("post.total_media_count == total_media_count: %s", instance.post.id)
#             media_paths = list(PostMedia.objects.filter(post=instance.post).values_list('absolute_media_path', flat=True))
#             if instance.post.group:
#                 send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: {instance.post.group.id}\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)
#                 logger.info("post with group has been sent to the admin: %s", instance.post.id)
#             else:
#                 send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: None\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)
#                 logger.info("post without group has been sent to the admin: %s", instance.post.id)
#         else:
#             logger.info("post.total_media_count != total_media_count: %s", instance.post.id)

# @receiver(post_delete, sender=PostMedia)
# def post_deleted(sender, instance, **kwargs):
#     post = instance.post
#     send_post_sync = async_to_sync(send_post)
#     # Проверяем, все ли медиа-файлы загружены для данного поста
#     total_media_count = post.mediafiles.count()
#     if post.total_media_count == total_media_count:
#         logger.info("delete media: post.total_media_count == total_media_count: %s", instance.post.id)
#         media_paths = list(PostMedia.objects.filter(post=instance.post).values_list('absolute_media_path', flat=True))
#         if instance.post.group:
#             send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: {instance.post.group.id}\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)
#             logger.info("delete media: post with group has been sent to the admin: %s", instance.post.id)
#         else:
#             send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: None\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)
#             logger.info("delete media: post without group has been sent to the admin: %s", instance.post.id)



# @receiver(pre_save, sender=Post)
# def post_edited(sender, instance, **kwargs):
#     send_post_sync = async_to_sync(send_post)
#     if instance.id is not None:
#         previous = Post.objects.get(id=instance.id)
#         if instance.approved!=True and previous.total_media_count==instance.total_media_count:
#             media_paths = list(Post.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
#             if instance.group:
#                 send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: {instance.group.id}\nUser ID: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
#                 logger.info("edit: post with group has been sent to the admin: %s", instance.id)
#             else:
#                 send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
#                 logger.info("edit: post without group has been sent to the admin: %s", instance.id)


# @receiver(post_save, sender=Post)
# def post_without_media_created(sender, created, instance, **kwargs):
#     send_post_sync = async_to_sync(send_post)
#     if created:
#         if instance.total_media_count==0:
#             if instance.group:
#                 send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
#                 logger.info("post with group has been sent to the admin: %s", instance.id)
#             else:
#                 send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})')
#                 logger.info("post without group has been sent to the admin: %s", instance.id)



@receiver(post_save, sender=Post)
def post_created(sender, created, instance, **kwargs):
    if not created:
        print('ok')
        send_post_sync = async_to_sync(send_post)
        if instance.approved==False:
            media_paths = list(Post.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
            if instance.group:
                send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: {instance.group.id}\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                logger.info("post with group has been sent to the admin: %s", instance.id)
            else:
                send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                logger.info("post without group has been sent to the admin: %s", instance.id)
