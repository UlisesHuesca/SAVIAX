# Generated by Django 3.2.5 on 2022-07-13 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_tipo_perfil_crear_sol'),
    ]

    operations = [
        migrations.AddField(
            model_name='distrito',
            name='abreviado',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
