# Generated by Django 4.2.4 on 2023-08-16 14:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_product_hide"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="second_hand",
        ),
    ]
