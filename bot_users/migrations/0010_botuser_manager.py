# Generated by Django 4.2.4 on 2023-08-10 05:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot_users", "0009_remove_botuser_updated_at_botuser_last_interaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="botuser",
            name="manager",
            field=models.BooleanField(default=False),
        ),
    ]
