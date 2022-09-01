from django.contrib import admin
from .models import Entrada, EntradaArticulo

# Register your models here.
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id','almacenista','oc','completo')
    list_filter = ('oc',)

class EntradaArticuloAdmin(admin.ModelAdmin):
    list_display = ('id','entrada','cantidad','articulo_comprado')
    list_filter = ('entrada',)

admin.site.register(Entrada, EntradaAdmin)

admin.site.register(EntradaArticulo, EntradaArticuloAdmin)