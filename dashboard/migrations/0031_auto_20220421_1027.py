# Generated by Django 3.2.5 on 2022-04-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_alter_order_approved_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='approved_at_time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='approved_at',
            field=models.DateField(auto_now=True),
        ),
    ]
