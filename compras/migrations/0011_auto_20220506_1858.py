# Generated by Django 3.2.5 on 2022-05-06 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0010_auto_20220506_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compra',
            old_name='oc_autorizada_por',
            new_name='oc_autorpor',
        ),
        migrations.RenameField(
            model_name='compra',
            old_name='oc_autorizada_por2',
            new_name='oc_autorpor2',
        ),
        migrations.RenameField(
            model_name='historicalcompra',
            old_name='oc_autorizada_por',
            new_name='oc_autorpor',
        ),
        migrations.RenameField(
            model_name='historicalcompra',
            old_name='oc_autorizada_por2',
            new_name='oc_autorpor2',
        ),
    ]
