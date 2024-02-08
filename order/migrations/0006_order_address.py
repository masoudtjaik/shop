# Generated by Django 5.0.1 on 2024-02-07 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_user_birthday_alter_user_is_active'),
        ('order', '0005_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default='tehran', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='account.address'),
        ),
    ]
