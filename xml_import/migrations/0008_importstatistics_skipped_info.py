# Generated by Django 4.2.4 on 2024-03-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("xml_import", "0007_alter_importstatistics_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="importstatistics",
            name="skipped_info",
            field=models.TextField(
                default="", verbose_name="Информация о пропущенных товарах"
            ),
        ),
    ]
