# Generated by Django 4.2.4 on 2023-08-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot_users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="botuser",
            name="user_id",
            field=models.CharField(default=123, max_length=256),
            preserve_default=False,
        ),
    ]
