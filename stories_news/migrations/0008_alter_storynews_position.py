# Generated by Django 4.2.4 on 2023-08-17 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stories_news", "0007_storynews_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storynews",
            name="position",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Номер позиции"
            ),
        ),
    ]
