from django.contrib import admin
from .models import Solicitud_Gasto, Articulo_Gasto, Tipo_Gasto, Entrada_Gasto_Ajuste, Conceptos_Entradas, Factura
# Register your models here.
class Solicitud_Gasto_Admin(admin.ModelAdmin):
    list_display = ('id','staff','colaborador', 'superintendente','autorizar','autorizar2','pagada')
    #list_filter = ('familia',)
    search_fields = ('colaborador',)

class Articulo_Gasto_Admin(admin.ModelAdmin):
    list_display =('id','staff','proyecto', 'subproyecto','producto','comentario', 'gasto', 'created_at', 'validacion')

class Entrada_Gasto_Ajuste_Admin(admin.ModelAdmin):
    list_display =('id','gasto','almacenista','completo')

class Factura_Admin(admin.ModelAdmin):
    list_display = ('solicitud_gasto', 'fecha_subida')

admin.site.register(Solicitud_Gasto, Solicitud_Gasto_Admin)

admin.site.register(Articulo_Gasto, Articulo_Gasto_Admin)

admin.site.register(Tipo_Gasto)

admin.site.register(Entrada_Gasto_Ajuste, Entrada_Gasto_Ajuste_Admin)

admin.site.register(Conceptos_Entradas)

admin.site.register(Factura, Factura_Admin)