# Generated by Django 5.0.6 on 2024-07-02 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0003_order_track_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="cancel_status",
            field=models.CharField(
                choices=[
                    ("processing", "processing"),
                    ("Approved", "Approved"),
                    ("NotApproved", "NotApproved"),
                ],
                max_length=20,
            ),
        ),
    ]
