# Generated by Django 4.2.1 on 2023-10-27 03:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0019_merge_20231026_2226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicaldata",
            name="birth_date",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="collection_record_date",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="commercial_premium",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="consultant",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="consultant_type",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="currency",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="dolar_commission",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="dolar_premium",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="email",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="expiration_date_first_coupon",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="final_validity",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="initial_validity",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="insurance_plan",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="insurance_vehicle",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="insured_amount",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="issuance_date",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="kcs_commission_percentage",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="months",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="net_commission_amount",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="net_premium",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="observations",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="payment_date",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="payment_document",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="payment_method",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="payment_status_first_coupon",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="phone_number",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="phone_number2",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="policy",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="policy_address",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="register_date",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="risk",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="status",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="total_premium",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="historicaldata",
            name="year",
            field=models.CharField(max_length=128, null=True),
        ),
    ]
