# Generated by Django 4.2.4 on 2023-08-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0020_alter_product_photo_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="currency",
            field=models.CharField(
                choices=[
                    ("RUB", "rub"),
                    ("USD", "usd"),
                    ("EUR", "eur"),
                    ("CNY", "cny"),
                ],
                default="RUB",
                max_length=3,
                verbose_name="Валюта",
            ),
        ),
    ]
