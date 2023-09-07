from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import BotUser
from bot.django_services import register_manager  # Замените на фактический путь
from asgiref.sync import async_to_sync

@receiver(pre_save, sender=BotUser)
def bot_user_manager_changed(sender, instance, **kwargs):
    if instance.id is not None:
        previous = BotUser.objects.get(id=instance.id)
        if not previous.manager and instance.manager:
            register_manager_sync = async_to_sync(register_manager)
            register_manager_sync(instance.user_id)
