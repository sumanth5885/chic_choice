# Generated by Django 4.2.2 on 2023-06-22 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_designer"),
    ]

    operations = [
        migrations.AddField(
            model_name="designer",
            name="designer_image",
            field=models.ImageField(default=0, upload_to="designerimg"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="designer",
            name="full_name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]