# Generated by Django 4.2.1 on 2023-10-26 02:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0015_issuanceinsurancevehicleendorsement"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalData",
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
                ("register_date", models.DateField(null=True)),
                ("collection_record_date", models.DateField(null=True)),
                ("customer", models.CharField(max_length=128, null=True)),
                (
                    "document_number",
                    models.CharField(max_length=32, null=True),
                ),
                ("birth_date", models.DateField(null=True)),
                ("consultant", models.CharField(max_length=64, null=True)),
                (
                    "consultant_type",
                    models.CharField(max_length=64, null=True),
                ),
                ("risk", models.CharField(max_length=64, null=True)),
                ("policy", models.CharField(max_length=64, null=True)),
                ("insurance_plan", models.CharField(max_length=64, null=True)),
                (
                    "insurance_vehicle",
                    models.CharField(max_length=64, null=True),
                ),
                ("issuance_date", models.DateField(null=True)),
                (
                    "payment_document",
                    models.CharField(max_length=64, null=True),
                ),
                ("expiration_date_first_coupon", models.DateField(null=True)),
                ("initial_validity", models.DateField(null=True)),
                ("final_validity", models.DateField(null=True)),
                ("payment_date", models.DateField(null=True)),
                (
                    "payment_status_first_coupon",
                    models.CharField(max_length=64, null=True),
                ),
                ("currency", models.CharField(max_length=64, null=True)),
                ("status", models.CharField(max_length=64, null=True)),
                ("observations", models.CharField(max_length=64, null=True)),
                ("insured_amount", models.CharField(max_length=64, null=True)),
                (
                    "kcs_commission_percentage",
                    models.CharField(max_length=64, null=True),
                ),
                ("net_premium", models.CharField(max_length=64, null=True)),
                (
                    "commercial_premium",
                    models.CharField(max_length=64, null=True),
                ),
                ("total_premium", models.CharField(max_length=64, null=True)),
                (
                    "net_commission_amount",
                    models.CharField(max_length=64, null=True),
                ),
                ("payment_method", models.CharField(max_length=64, null=True)),
                ("months", models.CharField(max_length=64, null=True)),
                ("year", models.CharField(max_length=64, null=True)),
                ("dolar_premium", models.CharField(max_length=64, null=True)),
                (
                    "dolar_commission",
                    models.CharField(max_length=64, null=True),
                ),
                ("email", models.CharField(max_length=64, null=True)),
                ("policy_address", models.CharField(max_length=64, null=True)),
                ("phone_number", models.CharField(max_length=64, null=True)),
                ("phone_number2", models.CharField(max_length=64, null=True)),
            ],
        ),
    ]
