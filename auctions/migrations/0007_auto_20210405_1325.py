# Generated by Django 3.1.7 on 2021-04-05 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_smalldescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='description',
            field=models.TextField(),
        ),
    ]
