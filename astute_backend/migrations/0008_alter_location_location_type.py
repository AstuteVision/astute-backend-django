# Generated by Django 4.2.6 on 2023-10-19 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('astute_backend', '0007_locationtype_location_location_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.ForeignKey(default='3009d864-634c-4cec-aa36-abb33231dff4', on_delete=django.db.models.deletion.CASCADE, to='astute_backend.locationtype'),
        ),
    ]
