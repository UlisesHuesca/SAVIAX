# Generated by Django 3.2.5 on 2022-05-31 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0039_auto_20220530_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='factura_pdf',
            field=models.FileField(blank=True, null=True, upload_to='facturas'),
        ),
        migrations.AlterField(
            model_name='historicalcompra',
            name='factura_pdf',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
