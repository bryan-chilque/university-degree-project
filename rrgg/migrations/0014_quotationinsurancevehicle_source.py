# Generated by Django 4.2.1 on 2023-10-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "rrgg",
            (
                "0013_quotationinsurancevehiclepremium_emission_right"
                "_percentage_and_more"
            ),
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="quotationinsurancevehicle",
            name="source",
            field=models.CharField(
                default="quotation", max_length=64, verbose_name="source"
            ),
            preserve_default=False,
        ),
    ]