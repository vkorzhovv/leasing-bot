# Generated by Django 4.2.4 on 2023-08-17 07:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_product_category2_alter_product_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="category2",
        ),
    ]
