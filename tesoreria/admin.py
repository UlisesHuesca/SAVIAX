from django.contrib import admin
from .models import Cuenta, Pago, Facturas

class PagoAdmin(admin.ModelAdmin):
    list_display = ('id','oc','gasto','viatico','tesorero','monto', 'hecho')
    #list_filter = ('familia',)
    search_fields = ['id','hecho','oc__folio','viatico__folio', 'gasto__folio','cuenta__cuenta']

# Register your models here.
admin.site.register(Cuenta)

admin.site.register(Facturas)

admin.site.register(Pago, PagoAdmin)