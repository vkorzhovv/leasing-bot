# Generated by Django 4.2.4 on 2023-08-16 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stories_news", "0005_storynews_approved"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="storynews",
            options={
                "verbose_name": "Актуальное/Новость",
                "verbose_name_plural": "Актуальное/Новости",
            },
        ),
        migrations.AlterField(
            model_name="storynews",
            name="approved",
            field=models.BooleanField(default=False, verbose_name="Подтверждено"),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="name",
            field=models.CharField(max_length=64, verbose_name="Заголовок"),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Фотография"
            ),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="sort",
            field=models.CharField(
                choices=[("news", "Новость"), ("story", "Актуальное")],
                max_length=10,
                verbose_name="Актуальное/Новость",
            ),
        ),
        migrations.AlterField(
            model_name="storynews",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Менеджер",
            ),
        ),
    ]
