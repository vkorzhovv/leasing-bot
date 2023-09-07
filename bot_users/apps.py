from django.apps import AppConfig


class BotUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot_users"
    verbose_name = "Пользователи бота"

    def ready(self):
            import bot_users.signals
