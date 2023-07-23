# Generated by Django 4.2.1 on 2023-07-22 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "rrgg",
            (
                "0025_rename_business_premium_insurancevehiclepremium"
                "_amount_and_more"
            ),
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="quotationinsurancevehicle",
            name="consultant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="consultants",
                to="rrgg.consultant",
            ),
        ),
        migrations.AlterField(
            model_name="quotationinsurancevehicle",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="vehicles",
                to="rrgg.vehicle",
            ),
        ),
    ]