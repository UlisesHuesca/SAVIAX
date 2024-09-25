from django.db import models
from dashboard.models import Inventario, Marca
from user.models import Profile
from django.core.validators import FileExtensionValidator
from simple_history.models import HistoricalRecords
# Create your models here.
class Tipo_Activo(models.Model):
    nombre = models.CharField(max_length= 100, null=True)

    def __str__(self):
        return f'{self.nombre}'


class Estatus_Activo(models.Model):
    nombre = models.CharField(max_length= 30, null=True)

    def __str__(self):
        return f'{self.nombre}'
    
class Activo(models.Model):
    activo = models.ForeignKey(Inventario, on_delete = models.CASCADE, null=True)
    tipo_activo = models.ForeignKey(Tipo_Activo, on_delete=models.CASCADE, null=True)
    responsable = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    creado_por = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='Creado_por')
    eco_unidad = models.CharField(max_length=50, null=True, unique=True)
    serie = models.CharField(max_length=20, null=True, unique=True)
    cuenta_contable = models.CharField(max_length=20, null=True)
    factura_interna = models.CharField(max_length=20, null=True)
    descripcion = models.CharField(max_length=100, null=True)
    marca = models.ForeignKey(Marca, on_delete = models.CASCADE, null=True)
    modelo = models.CharField(max_length=30, null=True, blank=True)
    estatus = models.ForeignKey(Estatus_Activo, on_delete = models.CASCADE, default=1)
    #codigo = models.CharField(max_length=20, null=True)
    comentario = models.CharField(max_length=100, null=True)
    fecha_asignacion = models.DateField(null=True, blank= True)
    completo = models.BooleanField(default=False)
    factura_pdf = models.FileField(blank=True, null=True, upload_to='pdf_activos',validators=[FileExtensionValidator(['pdf'])])
    factura_xml = models.FileField(blank=True, null=True, upload_to='xml_activos', validators=[FileExtensionValidator(['xml'])])
    documento_baja = models.FileField(blank=True, null=True, upload_to='bajas_activos',validators=[FileExtensionValidator(['pdf'])])
    modified_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='modified_by')
    modified_at = models.DateField(null=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    def __str__(self):
        return f'{self.eco_unidad}'
    
