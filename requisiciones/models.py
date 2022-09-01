from django.db import models
from dashboard.models import Order, Inventario, ArticulosparaSurtir
from user.models import Profile
from simple_history.models import HistoricalRecords

# Create your models here.
class Requis(models.Model):
    orden = models.ForeignKey(Order, on_delete = models.CASCADE, null = True)
    folio = models.CharField(max_length=7, blank=True, null=True)
    colocada = models.BooleanField(default=False)
    complete = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    requi_autorizada_por = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
    autorizar = models.BooleanField(null=True, default=None)
    approved_at = models.DateField(null=True)
    approved_at_time = models.TimeField(null=True)

    def __str__(self):
        return f'{self.get_folio} order {self.orden} req {self.id}'

    @property
    def get_folio(self):
        return str(self.pk).zfill(6)


class ArticulosRequisitados(models.Model):
    producto = models.ForeignKey(ArticulosparaSurtir, on_delete = models.CASCADE, null=True)
    req = models.ForeignKey(Requis, on_delete = models.CASCADE, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    cantidad_comprada = models.IntegerField(default=0, null=True, blank=True)
    art_surtido = models.BooleanField(null=True, default=False)
    almacenista = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, blank=True, related_name='Almacen2')
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    sel_comp = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.req} - {self.producto}- {self.cantidad}'

class Salidas(models.Model):
    almacenista = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Almacen')
    producto = models.ForeignKey(ArticulosparaSurtir, on_delete = models.CASCADE, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    comentario = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))
    material_recibido_por = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name='Salidas')
    salida_firmada = models.BooleanField(null=True, default=False)


    def __str__(self):
        return f'{self.producto} - {self.cantidad} - {self.created_at}'