# Generated by Django 4.2.2 on 2023-06-16 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0004_bcart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[
                    ("MB", "men-blazers"),
                    ("MST", "men-shirts"),
                    ("MP", "men-pants"),
                    ("MS", "men-shoes"),
                    ("MH", "men-hats"),
                    ("MEW", "men-eye-wears"),
                    ("TW", "top-wear"),
                    ("BW", "bottom-wear"),
                    ("C", "Chudidar"),
                    ("WS", "women-shoes"),
                    ("J", "jewellery"),
                    ("S", "saree"),
                    ("B", "boy"),
                    ("G", "girl"),
                ],
                max_length=4,
            ),
        ),
        migrations.CreateModel(
            name="Designer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]