# Generated by Django 4.2.2 on 2023-06-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0014_alter_designer_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="designer",
            name="des_category",
            field=models.CharField(
                choices=[("MD", "men-designers"), ("WD", "women-designers")],
                default=0,
                max_length=4,
            ),
            preserve_default=False,
        ),
    ]