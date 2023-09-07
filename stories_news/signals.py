from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoryNews
from bot.django_services import send_storynews_admin
from asgiref.sync import async_to_sync


@receiver(post_save, sender=StoryNews)
def post_created(sender, instance, **kwargs):
    if instance.id is not None:
        previous = StoryNews.objects.get(id=instance.id)
        if not (previous.approved == instance.approved and previous.approved==True):
            send_storynews_admin_sync = async_to_sync(send_storynews_admin)
            send_storynews_admin_sync(instance, instance.user.extended_user.bot_user.user_id)
