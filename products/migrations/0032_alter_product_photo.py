# Generated by Django 4.2.4 on 2024-02-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0031_alter_product_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="images", verbose_name="Фотография"
            ),
        ),
    ]