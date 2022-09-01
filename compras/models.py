from django.db import models
from dashboard.models import Order, Inventario, ArticulosparaSurtir
from requisiciones.models import Requis, ArticulosRequisitados
from user.models import Profile, Distrito
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords
from django.core.validators import FileExtensionValidator
# Create your models here.

class Banco(models.Model):
    nombre = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class Estatus_proveedor(models.Model):
    nombre = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return f'{self.nombre}'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=True, unique=True)
    rfc = models.CharField(max_length=13, null=True, unique=True)

    def __str__(self):
        return f'{self.nombre}'

class Proveedor_completo(models.Model):
    nombre = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=True)
    domicilio = models.CharField(max_length=200, null=True)
    contacto = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, null=True)
    clabe = models.CharField(max_length=20, null=True)
    cuenta = models.CharField(max_length=20, null=True)
    financiamiento = models.BooleanField(null=True, default=False)
    dias_credito = models.PositiveIntegerField(null=True)
    estatus = models.ForeignKey(Estatus_proveedor, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    def __str__(self):
        return f'{self.nombre}'

class Uso_cfdi(models.Model):
    codigo = models.CharField(max_length=3, null=True)
    descripcion = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

class Cond_credito(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre}'

class Moneda(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre}'

class Compra(models.Model):
    req = models.ForeignKey(Requis, on_delete = models.CASCADE, null=True)
    folio = models.CharField(max_length=7, null=True)
    complete = models.BooleanField(default=False)
    creada_por = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Generacion')
    created_at = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    oc_autorizada_por = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, blank=True, related_name='Aprobacion')
    autorizado_date1 = models.DateField(null=True, blank=True)
    autorizado_hora1 = models.TimeField(null=True, blank=True)
    autorizado1 = models.BooleanField(null=True, default=None)
    oc_autorizada_por2 = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, blank=True,related_name='Aprobacion2')
    autorizado_date2 = models.DateField(null=True, blank=True)
    autorizado_hora2 = models.TimeField(null=True, blank=True)
    autorizado2 = models.BooleanField(null=True, default=None)
    proveedor = models.ForeignKey(Proveedor_completo, on_delete = models.CASCADE, null=True, blank=True)
    cond_de_pago = models.ForeignKey(Cond_credito, on_delete = models.CASCADE, null=True, blank=True)
    uso_del_cfdi = models.ForeignKey(Uso_cfdi, on_delete = models.CASCADE, null=True, blank=True)
    dias_de_credito =  models.PositiveIntegerField(null=True, blank=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True)
    tipo_de_cambio = MoneyField(max_digits=14, decimal_places=4, null=True, blank=True, default_currency= 'MXN')
    anticipo = models.BooleanField(default=False)
    monto_anticipo = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    dias_de_entrega = models.PositiveIntegerField(null=True, blank=True)
    impuesto =  models.BooleanField(default=False)
    impuestos_adicionales = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    flete = models.BooleanField(default=False)
    costo_fletes = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    tesoreria_matriz = models.BooleanField(default=False)
    opciones_condiciones = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    factura_pdf = models.FileField(blank=True, null=True, upload_to='facturas',validators=[FileExtensionValidator(['pdf'])])
    factura_xml = models.FileField(blank=True, null=True, upload_to='xml', validators=[FileExtensionValidator(['xml'])])
    costo_oc = MoneyField(max_digits=14,decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    costo_iva = MoneyField(max_digits=14,decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    pagada = models.BooleanField(default=False)
    monto_pagado = MoneyField(max_digits=14,decimal_places=2, default=0, default_currency= 'MXN')
    entrada_completa = models.BooleanField(default=False)

    def __str__(self):
        return f'oc:{self.folio} - {self.id} - req:{self.req.folio} - sol:{self.req.orden.folio}'


class ArticuloComprado(models.Model):
    producto = models.ForeignKey(ArticulosRequisitados, on_delete = models.CASCADE, null=True)
    oc = models.ForeignKey(Compra, on_delete = models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    cantidad_pendiente = models.PositiveIntegerField(null=True, blank=True)
    entrada_completa = models.BooleanField(default=False)
    precio_unitario = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    def __str__(self):
        return f'{self.id} - {self.producto.producto.articulos.producto.producto} - {self.oc.id} - {self.cantidad} - {self.precio_unitario}'


