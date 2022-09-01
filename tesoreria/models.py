from django.db import models
from compras.models import Compra, ArticuloComprado, Proveedor_completo, Banco, Moneda
from user.models import Profile, Distrito
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords
from django.core.validators import FileExtensionValidator
# Create your models here.

class Cuenta(models.Model):
    cuenta = models.CharField(max_length=13, null=True)
    clabe = models.CharField(max_length=22, null=True)
    distrito = models.ForeignKey(Distrito, on_delete = models.CASCADE, null=True)
    encargado = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    banco = models.ForeignKey(Banco, on_delete = models.CASCADE, null=True)
    monto_inicial = MoneyField(max_digits=14,decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    saldo = MoneyField(max_digits=14,decimal_places=2, null=True, blank=True, default_currency= 'MXN')
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.cuenta} - {self.monto_inicial}'

class Pago(models.Model):
    tesorero = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Tesorero')
    oc = models.ForeignKey(Compra, on_delete = models.CASCADE, null=True)
    cuenta = models.ForeignKey (Cuenta, on_delete = models.CASCADE, null=True)
    monto = MoneyField(max_digits=14,decimal_places=2, default_currency= 'MXN')
    distrito = models.ForeignKey(Distrito, on_delete = models.CASCADE, null=True)
    comentario = models.CharField(max_length=100, null=True, blank=True)
    pagado_date = models.DateField(null=True, blank=True)
    pagado_hora = models.TimeField(null=True, blank=True)
    hecho = models.BooleanField(default=False)
    tipo_de_cambio = MoneyField(max_digits=14,decimal_places=4, null=True, blank=True, default_currency= 'MXN')
    comprobante_pago = models.FileField(null=True, upload_to='comprobante',validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return f'{self.id} - {self.oc} - {self.cuenta}'
