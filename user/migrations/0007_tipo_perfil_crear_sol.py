# Generated by Django 3.2.5 on 2022-04-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20220426_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo_perfil',
            name='crear_sol',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
