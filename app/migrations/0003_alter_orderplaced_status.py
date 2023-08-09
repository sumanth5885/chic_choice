# Generated by Django 4.2.2 on 2023-06-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_rename_product_image_product_product_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplaced",
            name="status",
            field=models.CharField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("Packed", "Packed"),
                    ("On The Way", "On The Way"),
                    ("Delivered", "Delivered"),
                    ("Cancel", "Cancel"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]
