# Generated by Django 5.1 on 2024-08-29 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abacusapp', '0004_alter_price_asset_alter_price_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioassetquantity',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
