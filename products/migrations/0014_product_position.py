# Generated by Django 4.2.4 on 2023-08-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0013_remove_product_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="position",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Номер позиции в категории"
            ),
        ),
    ]
