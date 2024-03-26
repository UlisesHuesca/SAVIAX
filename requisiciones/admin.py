from django.contrib import admin
from .models import Salidas, Requis, ArticulosRequisitados, ValeSalidas, Devolucion, Devolucion_Articulos, Tipo_Devolucion

class RequisAdmin(admin.ModelAdmin):
    list_display = ('id','folio','orden','autorizar')
    list_filter = ('folio',)

class ValeSalidasAdmin(admin.ModelAdmin):
    list_display = ('id','solicitud','complete','created_at')

class Articulos_RequisitadosAdmin(admin.ModelAdmin):
    list_display = ('req','producto','cantidad')
    search_fields = ['producto__articulos__producto__producto__nombre','req__folio']
    raw_id_fields = ('req','producto')

class SalidasAdmin(admin.ModelAdmin):
    list_display = ('id','producto','cantidad','precio','complete','entrada')
    search_fields = ['producto__articulos__producto__producto__nombre']

class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('id','solicitud','almacenista','autorizada')
    raw_id_fields = ('solicitud','almacenista','producto',)

class Devolucion_ArticulosAdmin(admin.ModelAdmin):
    list_display = ('vale_devolucion','producto','cantidad','precio','comentario')
    search_fields = ['producto__articulos__producto__producto__nombre']
    raw_id_fields = ('vale_devolucion','producto',)


class Tipo_Admin(admin.ModelAdmin):
    list_display = ('id','nombre')

# Register your models here.
admin.site.register(Salidas, SalidasAdmin)

admin.site.register(ValeSalidas, ValeSalidasAdmin)

admin.site.register(Tipo_Devolucion, Tipo_Admin)

admin.site.register(Requis, RequisAdmin)

admin.site.register(ArticulosRequisitados, Articulos_RequisitadosAdmin)

admin.site.register(Devolucion, DevolucionAdmin)

admin.site.register(Devolucion_Articulos, Devolucion_ArticulosAdmin)