# Generated by Django 3.2.5 on 2023-08-10 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_proyecto_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta_Contable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('descripcion', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='cuenta_contable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.cuenta_contable'),
        ),
    ]
