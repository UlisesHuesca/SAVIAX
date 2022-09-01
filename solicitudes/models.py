from django.db import models
# De django.contrib.auth.models estamos importando el modelo de usuarios de la administration
from django.contrib.auth.models import User
from user.models import Distrito
from djmoney.models.fields import MoneyField

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nombre', 'distrito',)

    def get_projects_total(self):
        subproyectos = self.subproyecto_set.all()
        total = sum([subproyecto.presupueto for subproyecto in subproyectos])
        return total

    def __str__(self):
        return f'{self.nombre}-{self.distrito}'

class Subproyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete = models.CASCADE, null=True)
    nombre = models.CharField(max_length=50, null=True, unique=True)
    presupuesto = MoneyField(max_digits=14, decimal_places=2, null=True,default_currency= 'MXN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gastado = MoneyField(max_digits=14, decimal_places=2, default=0,default_currency= 'MXN')

    def __str__(self):
        return f'{self.nombre}-{self.presupuesto}'

class Sector(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}'

class Activo(models.Model):
    eco_unidad = models.CharField(max_length=15, null=True, unique=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=15, null=True)
    serie = models.CharField(max_length=15, null=True)
    cuenta = models.CharField(max_length=15, null=True)
    factura_interna = models.CharField(max_length=15, null=True)
    arrendado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.eco_unidad}'

class Operacion(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}'



