import django_filters
from requisiciones.models import ArticulosRequisitados
from .models import Entrada, EntradaArticulo
from django_filters import CharFilter, DateFilter
from django.db.models import Q

class EntradaArticuloFilter(django_filters.FilterSet):
    #producto = CharFilter(field_name='articulo_comprado__producto__producto__articulos__producto__producto__nombre', lookup_expr='icontains')
    proveedor = CharFilter(field_name='entrada__oc__proveedor__nombre__razon_social', lookup_expr='icontains')
    oc = CharFilter(field_name='entrada__oc__id', lookup_expr='icontains')
    req = CharFilter(field_name='entrada__oc__req__id', lookup_expr='icontains')
    start_date = DateFilter(field_name = 'entrada__date', lookup_expr='gte')
    end_date = DateFilter(field_name='entrada__date',lookup_expr='lte')
    proyecto = CharFilter(field_name='entrada__oc__req__orden__proyecto__nombre', lookup_expr='icontains')
    subproyecto = CharFilter(field_name='entrada__oc__req__orden__subproyecto__nombre', lookup_expr='icontains')

    class Meta:
        model = EntradaArticulo
        fields = ['oc','proveedor','start_date','end_date','req','proyecto','subproyecto'] #'producto'
