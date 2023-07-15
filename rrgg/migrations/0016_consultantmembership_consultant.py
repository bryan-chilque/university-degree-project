# Generated by Django 4.2.1 on 2023-07-15 16:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rrgg", "0015_alter_consultant_document_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultantmembership",
            name="consultant",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="membership",
                to="rrgg.consultant",
            ),
            preserve_default=False,
        ),
    ]
