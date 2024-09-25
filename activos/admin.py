from django.contrib import admin
from .models import Activo, Tipo_Activo, Estatus_Activo
# Register your models here.
class Tipo_Activo_Admin(admin.ModelAdmin):
    list_display = ('nombre',)
    #search_fields = ('oc',)

class ActivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'activo', 'responsable')
    search_fields = ['responsable']
    raw_id_fields = ('activo',)  # Corregido

admin.site.register(Activo, ActivoAdmin)
admin.site.register(Estatus_Activo)

admin.site.register(Tipo_Activo, Tipo_Activo_Admin)