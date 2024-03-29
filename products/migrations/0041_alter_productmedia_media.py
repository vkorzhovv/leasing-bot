# Generated by Django 4.2.4 on 2024-03-14 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0040_alter_product_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmedia",
            name="media",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="media/share_images/",
                verbose_name="Доп. фотки",
            ),
        ),
    ]
