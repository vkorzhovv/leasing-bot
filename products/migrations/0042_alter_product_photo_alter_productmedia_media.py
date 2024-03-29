# Generated by Django 4.2.4 on 2024-03-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0041_alter_productmedia_media"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="share_images/", verbose_name="Фотография"
            ),
        ),
        migrations.AlterField(
            model_name="productmedia",
            name="media",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="share_images/",
                verbose_name="Доп. фотки",
            ),
        ),
    ]
