# Generated by Django 3.1.7 on 2021-03-24 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
