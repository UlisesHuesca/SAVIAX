# Generated by Django 3.2.5 on 2023-07-30 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20230622_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulosordenados',
            name='comentario',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
