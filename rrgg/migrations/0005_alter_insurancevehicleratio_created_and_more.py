# Generated by Django 4.2.1 on 2023-09-06 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "rrgg",
            "0004_alter_collectioninsurancevehicle_expiration_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="insurancevehicleratio",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="quotationinsurancevehiclepremium",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="created at"
            ),
        ),
    ]
