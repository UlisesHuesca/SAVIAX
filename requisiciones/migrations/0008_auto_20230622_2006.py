# Generated by Django 3.2.5 on 2023-06-23 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisiciones', '0007_auto_20230526_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsalidas',
            name='comentario',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='salidas',
            name='comentario',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
