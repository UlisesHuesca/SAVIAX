# Generated by Django 3.2.5 on 2022-04-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_alter_order_autorizar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='autorizar',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
