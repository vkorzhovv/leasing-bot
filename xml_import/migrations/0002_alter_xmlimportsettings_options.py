# Generated by Django 4.2.4 on 2024-02-28 12:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("xml_import", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="xmlimportsettings",
            options={
                "verbose_name": "Настройки XML импорта",
                "verbose_name_plural": "Настройки XML импорта",
            },
        ),
    ]