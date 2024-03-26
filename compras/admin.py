from django.contrib import admin
from .models import Compra, ArticuloComprado, Proveedor, Proveedor_direcciones, Proveedor_Direcciones_Batch, Estatus_proveedor, Uso_cfdi, Cond_credito, Moneda, Estado, Comparativo, Item_Comparativo, Tipo_Evaluacion, Preevaluacion

class CompraAdmin(admin.ModelAdmin):
    list_display = ('id','folio', 'req','proveedor','oc_autorizada_por2','cond_de_pago','autorizado1','autorizado2')
    list_filter = ('proveedor',)

class ArticuloComprado_Admin(admin.ModelAdmin):
    list_display = ('oc','producto','cantidad')
    raw_id_fields = ['oc','producto'] 
    search_fields = ['producto__producto__articulos__producto__producto__nombre']
    raw_id_fields = ('producto',)

class ProveedorAdmin(admin.ModelAdmin):
    search_fields = ('razon_social',)

class Proveedor_direccionesAdmin(admin.ModelAdmin):
    search_fields = ('nombre__razon_social',)

class MonedaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')
# Register your models here.
admin.site.register(Compra, CompraAdmin)

admin.site.register(ArticuloComprado, ArticuloComprado_Admin)

admin.site.register(Proveedor, ProveedorAdmin)

admin.site.register(Proveedor_direcciones, Proveedor_direccionesAdmin)

admin.site.register(Estatus_proveedor)

admin.site.register(Proveedor_Direcciones_Batch)

admin.site.register(Uso_cfdi)

admin.site.register(Cond_credito)

admin.site.register(Moneda,MonedaAdmin)

admin.site.register(Estado)

admin.site.register(Comparativo)

admin.site.register(Item_Comparativo)

admin.site.register(Tipo_Evaluacion)

admin.site.register(Preevaluacion)