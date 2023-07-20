# Generated by Django 4.2.1 on 2023-07-15 16:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rrgg", "0014_alter_consultant_document_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consultant",
            name="document_number",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="document_number",
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name="insurancevehicle",
            name="name",
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="insurancevehicleprice",
            name="created",
            field=models.DateTimeField(auto_now_add=True, unique=True),
        ),
        migrations.CreateModel(
            name="ConsultantMembership",
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="membership",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
