# Generated by Django 4.2.4 on 2024-03-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0045_alter_product_char_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="char_id",
            field=models.CharField(
                max_length=128, 
                blank=True,
                editable=False,
                null=True,
                unique=True,
                verbose_name="Артикул",
            ),
        ),
    ]
