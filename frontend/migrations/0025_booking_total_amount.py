# Generated by Django 5.0.3 on 2025-03-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0024_user_details_travel_way'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
