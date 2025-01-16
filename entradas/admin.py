from django.contrib import admin
from .models import Entrada, EntradaArticulo, Reporte_Calidad, No_Conformidad, NC_Articulo, Tipo_Nc, Cierre_Nc

# Register your models here.
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'almacenista', 'oc', 'completo')
    #list_filter = ('oc',)
    search_fields = ['oc__id', 'oc__nombre'] 
    raw_id_fields = ('almacenista','oc')

class EntradaArticuloAdmin(admin.ModelAdmin):
    list_display = ('id','entrada','cantidad','articulo_comprado','liberado','cantidad_por_surtir')
    search_fields = ['articulo_comprado__producto__producto__articulos__producto__producto__nombre']
    raw_id_fields = ('articulo_comprado','entrada')

class NC_ArticuloAdmin(admin.ModelAdmin):
    list_display = ('id','nc','cantidad','articulo_comprado')
    search_fields = ['articulo_comprado']
    raw_id_fields = ('nc','articulo_comprado','entrada_articulo')

class No_ConformidadAdmin(admin.ModelAdmin):
    list_display = ('id','oc','tipo_nc')
    search_fields = ['oc']
    raw_id_fields = ('almacenista','oc')

class Reporte_CalidadAdmin(admin.ModelAdmin):
    list_display = ('id','articulo')
    search_fields = ['articulo']
    raw_id_fields = ('articulo',)

class Cierre_NcAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    

admin.site.register(Entrada, EntradaAdmin)

admin.site.register(EntradaArticulo, EntradaArticuloAdmin)

admin.site.register(Reporte_Calidad, Reporte_CalidadAdmin)

admin.site.register(No_Conformidad,No_ConformidadAdmin)

admin.site.register(NC_Articulo, NC_ArticuloAdmin)

admin.site.register(Tipo_Nc)

admin.site.register(Cierre_Nc,Cierre_NcAdmin)