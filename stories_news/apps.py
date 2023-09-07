from django.apps import AppConfig


class StoriesNewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stories_news"
    verbose_name = "Актуальное и новости"

    def ready(self):
            import stories_news.signals
