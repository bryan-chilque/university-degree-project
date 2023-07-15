# Generated by Django 4.2.1 on 2023-07-15 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrgg', '0008_remove_quotationinsurancevehicle_vehicle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationinsurancevehicle',
            name='vehicle',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='quotation_insurance_vehicle', to='rrgg.vehicle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quotationinsurancevehicle',
            name='consultant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='quotation_insurance_vehicle', to='rrgg.consultant'),
        ),
        migrations.AlterField(
            model_name='quotationinsurancevehicle',
            name='insurance_vehicle_price',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='quotation_insurance_vehicle', to='rrgg.insurancevehicleprice'),
        ),
    ]
