# Generated by Django 4.2.1 on 2023-08-12 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0044_remove_issuanceinsurancestatus_comment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                    "name",
                    models.CharField(
                        max_length=64,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
            ],
            options={
                "verbose_name": "role",
                "verbose_name_plural": "roles",
            },
        ),
        migrations.RemoveField(
            model_name="consultant",
            name="document_number",
        ),
        migrations.CreateModel(
            name="Area",
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
                    "name",
                    models.CharField(
                        max_length=64,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "consultant",
                    models.ManyToManyField(
                        related_name="area",
                        to="rrgg.consultant",
                        verbose_name="consultant",
                    ),
                ),
            ],
            options={
                "verbose_name": "area",
                "verbose_name_plural": "areas",
            },
        ),
        migrations.AddField(
            model_name="consultant",
            name="role",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="consultant",
                to="rrgg.role",
                verbose_name="role",
            ),
        ),
    ]