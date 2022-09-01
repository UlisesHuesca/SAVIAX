import django_filters
from .models import Compra
from django_filters import CharFilter, DateFilter

class PagoFilter(django_filters.FilterSet):
    oc = CharFilter(field_name='oc__id', lookup_expr='icontains')
    proveedor = CharFilter(field_name='oc__proveedor',lookup_expr='icontains')
    monto_pagado = CharFilter(field_name='monto_pagado', lookup_expr='icontains')
    proyecto = CharFilter(field_name='oc__req__orden__proyecto',lookup_expr='icontains')
    subproyecto = CharFilter(field_name='oc__req__orden__subproyecto', lookup_expr='icontains')
    solicitada_por = CharFilter(field_name='oc__req__orden__staff__staff', lookup_expr='icontains')
    start_date = DateFilter(field_name = 'pagado_date', lookup_expr='gte')
    end_date = DateFilter(field_name='pagado_date',lookup_expr='lte')
    cuenta = CharFilter(field_name='cuenta', lookup_expr='icontains')
    id = CharFilter(field_name='id', lookup_expr='icontains')

    class Meta:
        model = Compra
        fields = ['oc','proveedor','proyecto','subproyecto','monto_pagado','solicitada_por','start_date','end_date','cuenta','id',]
