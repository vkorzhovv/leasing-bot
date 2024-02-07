# Generated by Django 4.2.4 on 2024-02-06 12:26

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0038_alter_product_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="photo",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=["middle", "center"],
                force_format=None,
                keep_meta=True,
                quality=-1,
                scale=0.5,
                size=[1000, 500],
                upload_to="images",
                verbose_name="Фотография",
            ),
        ),
    ]
