# Generated by Django 3.2.5 on 2022-04-18 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_alter_order_sol_autorizada_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='approved_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
