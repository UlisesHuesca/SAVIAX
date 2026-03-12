from django.contrib import admin
from .models import Cuenta, Pago, Facturas

class FacturasAdmin(admin.ModelAdmin):
    search_fields = ['oc__folio','id','uuid']
    raw_id_fields = ('oc',)
    list_display = ('id','oc','factura_pdf','factura_xml','uuid')

class PagoAdmin(admin.ModelAdmin):
    list_display = ('id','oc','gasto','viatico','tesorero','monto', 'hecho')
    #list_filter = ('familia',)
    search_fields = ['id','hecho','oc__folio','viatico__folio', 'gasto__folio','cuenta__cuenta']

# Register your models here.
admin.site.register(Cuenta)

admin.site.register(Facturas, FacturasAdmin)

admin.site.register(Pago, PagoAdmin)