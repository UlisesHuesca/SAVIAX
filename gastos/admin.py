from django.contrib import admin
from .models import Solicitud_Gasto, Articulo_Gasto, Tipo_Gasto
# Register your models here.
admin.site.register(Solicitud_Gasto)

admin.site.register(Articulo_Gasto)

admin.site.register(Tipo_Gasto)