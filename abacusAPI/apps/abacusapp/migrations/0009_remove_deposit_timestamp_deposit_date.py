# Generated by Django 5.1 on 2024-08-29 02:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abacusapp', '0008_remove_deposit_date_deposit_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='deposit',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
