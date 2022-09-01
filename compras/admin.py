from django.contrib import admin
from .models import Compra, ArticuloComprado, Proveedor, Proveedor_completo, Estatus_proveedor, Banco, Uso_cfdi, Cond_credito, Moneda

class CompraAdmin(admin.ModelAdmin):
    list_display = ('id','folio', 'req','proveedor','autorizado1','autorizado2')
    list_filter = ('proveedor',)

# Register your models here.
admin.site.register(Compra, CompraAdmin)

admin.site.register(ArticuloComprado)

admin.site.register(Proveedor)

admin.site.register(Proveedor_completo)

admin.site.register(Estatus_proveedor)

admin.site.register(Banco)

admin.site.register(Uso_cfdi)

admin.site.register(Cond_credito)

admin.site.register(Moneda)

