# Generated by Django 3.2.5 on 2023-04-25 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('factura', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_factura', models.DateField(blank=True, null=True)),
                ('folio_cotizacion', models.CharField(blank=True, max_length=10, null=True)),
                ('oc_cliente', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=19, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.cliente')),
                ('distrito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.distrito')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='St_Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subproyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, unique=True)),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gastado', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('proyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.proyecto')),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='status_de_entrega',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.st_entrega'),
        ),
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eco_unidad', models.CharField(max_length=15, null=True, unique=True)),
                ('tipo', models.CharField(max_length=15, null=True)),
                ('serie', models.CharField(max_length=15, null=True)),
                ('cuenta', models.CharField(max_length=15, null=True)),
                ('factura_interna', models.CharField(max_length=15, null=True)),
                ('arrendado', models.BooleanField(default=True)),
                ('distrito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.distrito')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='proyecto',
            unique_together={('nombre', 'distrito')},
        ),
    ]
