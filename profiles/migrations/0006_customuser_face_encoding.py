# Generated by Django 5.1.1 on 2024-10-15 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0005_customuser_alter_log_user_alter_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="face_encoding",
            field=models.TextField(blank=True, null=True),
        ),
    ]
