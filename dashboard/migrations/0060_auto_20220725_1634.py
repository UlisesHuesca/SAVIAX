# Generated by Django 3.2.5 on 2022-07-25 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_auto_20220725_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalorder',
            name='surtida',
        ),
        migrations.RemoveField(
            model_name='order',
            name='surtida',
        ),
    ]
