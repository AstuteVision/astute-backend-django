# Generated by Django 4.2.6 on 2023-10-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField()),
                ('description', models.TextField()),
                ('coordinates_vertical', models.FloatField()),
                ('coordinates_horizontal', models.FloatField()),
                ('cost', models.FloatField()),
                ('comment', models.TextField()),
                ('category', models.TextField()),
                ('active', models.BooleanField()),
            ],
        ),
    ]
