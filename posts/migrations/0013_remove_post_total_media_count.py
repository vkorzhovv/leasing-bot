# Generated by Django 4.2.4 on 2023-10-10 12:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0012_alter_post_scheduled_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="total_media_count",
        ),
    ]