# Generated by Django 4.1.7 on 2023-04-10 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NSEAPP', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='target_price',
        ),
    ]
