# Generated by Django 4.2.1 on 2023-07-25 19:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0029_insurancevehicle_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="insurancevehicle",
            old_name="image",
            new_name="logo",
        ),
    ]
