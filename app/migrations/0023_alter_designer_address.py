# Generated by Django 4.2.2 on 2023-06-27 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0022_alter_designerplaced_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="designer",
            name="address",
            field=models.TextField(max_length=100, null=True),
        ),
    ]
