# Generated by Django 5.0.1 on 2024-02-07 15:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0046_alter_discount_expire_alter_discount_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 8, 15, 16, 52, 80156, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='discount',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 7, 15, 16, 52, 80156, tzinfo=datetime.timezone.utc)),
        ),
    ]
