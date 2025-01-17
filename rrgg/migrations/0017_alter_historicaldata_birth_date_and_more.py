# Generated by Django 4.2.1 on 2023-10-26 02:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0016_historicaldata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaldata",
            name="birth_date",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="collection_record_date",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="expiration_date_first_coupon",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="final_validity",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="initial_validity",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="issuance_date",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="payment_date",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="register_date",
            field=models.CharField(max_length=64, null=True),
        ),
    ]
