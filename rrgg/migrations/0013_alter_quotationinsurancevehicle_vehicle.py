# Generated by Django 4.2.1 on 2023-07-15 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0012_alter_quotationinsurancevehicle_vehicle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quotationinsurancevehicle",
            name="vehicle",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="quotation_insurance_vehicle",
                to="rrgg.vehicle",
            ),
        ),
    ]
