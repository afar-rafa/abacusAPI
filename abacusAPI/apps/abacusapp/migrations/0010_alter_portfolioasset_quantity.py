# Generated by Django 5.1 on 2024-08-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abacusapp', '0009_remove_deposit_timestamp_deposit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioasset',
            name='quantity',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]
