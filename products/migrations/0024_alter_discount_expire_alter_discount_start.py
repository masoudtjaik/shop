# Generated by Django 4.2.7 on 2024-01-14 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_alter_discount_expire_alter_discount_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 15, 11, 9, 58, 69690, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 14, 11, 7, 58, 69690, tzinfo=datetime.timezone.utc)),
        ),
    ]
