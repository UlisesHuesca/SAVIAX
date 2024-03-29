# Generated by Django 3.2.5 on 2023-08-10 23:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20230808_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='comentario',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='soporte',
            field=models.TextField(blank=True, max_length=100, null=True, validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AddField(
            model_name='order',
            name='comentario',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='soporte',
            field=models.FileField(blank=True, null=True, upload_to='facturas', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
