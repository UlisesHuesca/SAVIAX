# Generated by Django 3.2.5 on 2023-03-28 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_banco'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo_perfil',
            name='calidad',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
