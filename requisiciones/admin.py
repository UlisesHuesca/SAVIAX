from django.contrib import admin
from .models import Salidas, Requis, ArticulosRequisitados

class RequisAdmin(admin.ModelAdmin):
    list_display = ('id','folio','orden','autorizar')
    list_filter = ('folio',)

# Register your models here.
admin.site.register(Salidas)

admin.site.register(Requis, RequisAdmin)

admin.site.register(ArticulosRequisitados)