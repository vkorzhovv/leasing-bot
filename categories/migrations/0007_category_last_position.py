# Generated by Django 4.2.4 on 2024-02-19 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0006_alter_category_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="last_position",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Последняя позиция"
            ),
        ),
    ]
