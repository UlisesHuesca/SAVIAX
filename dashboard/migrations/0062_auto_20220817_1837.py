# Generated by Django 3.2.5 on 2022-08-17 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0061_auto_20220811_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorder',
            name='created_at',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='created_at_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at_time',
            field=models.TimeField(null=True),
        ),
    ]
