# Generated by Django 4.2.4 on 2023-08-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0018_product_category2"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="photo_url",
            field=models.CharField(
                blank=True,
                max_length=128,
                null=True,
                verbose_name="Адрес для яндекс-картинку",
            ),
        ),
    ]
