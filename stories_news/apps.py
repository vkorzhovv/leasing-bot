from django.apps import AppConfig


class StoriesNewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stories_news"
    verbose_name = "Актуальноые статусы и новости"

    def ready(self):
            import stories_news.signals
