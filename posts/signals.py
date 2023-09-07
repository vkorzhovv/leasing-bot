from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Post, PostMedia
from bot.django_services import send_post, get_post_path
from asgiref.sync import async_to_sync


@receiver(post_save, sender=PostMedia)
def post_created(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        send_post_sync = async_to_sync(send_post)
        # Проверяем, все ли медиа-файлы загружены для данного поста
        total_media_count = post.mediafiles.count()
        if post.total_media_count == total_media_count:
            media_paths = list(PostMedia.objects.filter(post=instance.post).values_list('absolute_media_path', flat=True))
            if instance.post.group:
                send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: {instance.post.group.id}\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)
            else:
                send_post_sync(f'ID поста: {instance.post.id}\nТекст поста: {instance.post.text}\nID группы: None\nТелеграм-ID менеджера: {instance.post.user.extended_user.bot_user.user_id} ({instance.post.user.extended_user.user.username}|запланировано на {instance.post.scheduled_time})', media_paths)


@receiver(post_save, sender=Post)
def post_edited(sender, created, instance, **kwargs):
    send_post_sync = async_to_sync(send_post)
    if not created:
        if instance.id is not None:
            previous = Post.objects.get(id=instance.id)
            if not (previous.approved == instance.approved and previous.approved==True):
                media_paths = list(Post.objects.get(pk=instance.id).mediafiles.all().values_list('absolute_media_path', flat=True))
                if instance.group:
                    send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: {instance.group.id}\nUser ID: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
                else:
                    send_post_sync(f'ID поста: {instance.id}\nТекст поста: {instance.text}\nID группы: None\nТелеграм-ID менеджера: {instance.user.extended_user.bot_user.user_id} ({instance.user.extended_user.user.username}|запланировано на {instance.scheduled_time})', media_paths)
