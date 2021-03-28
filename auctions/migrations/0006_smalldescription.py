# Generated by Django 3.1.7 on 2021-03-25 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_closeauction'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmallDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=64)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='small_description', to='auctions.listings')),
            ],
        ),
    ]