# Generated by Django 4.2.2 on 2023-06-16 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_rename_user_designer_username"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Designer",
        ),
    ]