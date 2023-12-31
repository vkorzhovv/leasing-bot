# Generated by Django 4.2.4 on 2023-09-28 06:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0029_productmedia_media_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmedia",
            name="media",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="product_media/",
                verbose_name="Доп. фотки",
            ),
        ),
    ]
