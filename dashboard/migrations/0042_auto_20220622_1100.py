# Generated by Django 3.2.5 on 2022-06-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_auto_20220614_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='approved_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='approved_at_time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
