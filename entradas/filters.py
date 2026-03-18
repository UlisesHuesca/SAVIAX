import django_filters 
from requisiciones.models import ArticulosRequisitados
from .models import Entrada, EntradaArticulo, No_Conformidad, Tipo_Nc, Cierre_Nc, Reporte_Calidad
from django_filters import CharFilter, DateFilter, ChoiceFilter
from django.db.models import Q

class EntradaArticuloFilter(django_filters.FilterSet):
    #producto = CharFilter(field_name='articulo_comprado__producto__producto__articulos__producto__producto__nombre', lookup_expr='icontains')
    proveedor = CharFilter(field_name='entrada__oc__proveedor__nombre__razon_social', lookup_expr='icontains')
    oc = CharFilter(field_name='entrada__oc__id', lookup_expr='icontains')
    req = CharFilter(field_name='entrada__oc__req__id', lookup_expr='icontains')
    start_date = DateFilter(field_name = 'entrada__entrada__date', lookup_expr='gte')
    end_date = DateFilter(field_name='entrada__entrada__date',lookup_expr='lte')
    proyecto = CharFilter(field_name='entrada__oc__req__orden__proyecto__nombre', lookup_expr='icontains')
    subproyecto = CharFilter(field_name='entrada__oc__req__orden__subproyecto__nombre', lookup_expr='icontains')

    class Meta:
        model = EntradaArticulo
        fields = ['oc','proveedor','start_date','end_date','req','proyecto','subproyecto'] #'producto'

class No_ConformidadFilter(django_filters.FilterSet):
    oc = CharFilter(field_name='oc__id', lookup_expr='icontains')
    tipo_nc = django_filters.ModelChoiceFilter(queryset=Tipo_Nc.objects.all(), label='Tipo NC')
    nc_date = DateFilter(field_name='nc_date', lookup_expr='exact', label='Fecha NC')
    cierre = django_filters.ModelChoiceFilter(queryset=Cierre_Nc.objects.all(), label='Cierre')
    proveedor = CharFilter(field_name='oc__proveedor__nombre__razon_social', lookup_expr='icontains')

    class Meta:
        model = No_Conformidad
        fields = ['oc','tipo_nc','nc_date','cierre',]

class Reporte_CalidadFilter(django_filters.FilterSet):
    autorizado_choices = [
            (True, 'Autorizado'),
            (False, 'No Autorizado'),
        ]
   
    #producto = CharFilter(field_name='articulo_comprado__producto__producto__articulos__producto__producto__nombre', lookup_expr='icontains')
    proveedor = CharFilter(field_name='articulo__entrada__oc__proveedor__nombre__razon_social', lookup_expr='icontains')
    oc = CharFilter(field_name='articulo__entrada__oc__id', lookup_expr='icontains')
    req = CharFilter(field_name='articulo__entrada__oc__req__id', lookup_expr='icontains')
    start_date = DateFilter(field_name = 'reporte_date', lookup_expr='gte')
    end_date = DateFilter(field_name='reporte_date',lookup_expr='lte')
    proyecto = CharFilter(field_name='articulo__entrada__oc__req__orden__proyecto__nombre', lookup_expr='icontains')
    subproyecto = CharFilter(field_name='articulo__entrada__oc__req__orden__subproyecto__nombre', lookup_expr='icontains')
    autorizado = ChoiceFilter(choices=autorizado_choices, empty_label='Todos', field_name='articulo__calidad')


    class Meta:
        model = Reporte_Calidad
        fields = ['articulo','reporte_date','autorizado'] #'producto'

class EntradaCaducidadFilter(django_filters.FilterSet):
    proveedor = CharFilter(field_name='entrada__oc__proveedor__nombre__razon_social', lookup_expr='icontains')
    oc = CharFilter(field_name='entrada__oc__id', lookup_expr='icontains')
    start_date = DateFilter(field_name='fecha_caducidad', lookup_expr='gte')
    end_date = DateFilter(field_name='fecha_caducidad', lookup_expr='lte')

    class Meta:
        model = EntradaArticulo
        fields = ['oc', 'proveedor', 'fecha_caducidad']

class EntradaTerminadoFilter(django_filters.FilterSet):
    solicitud = CharFilter(field_name='producto_terminado__solicitud__id', lookup_expr='icontains')
    proyecto = CharFilter(field_name='producto_terminado__solicitud__proyecto__nombre', lookup_expr='icontains')
    subproyecto = CharFilter(field_name='producto_terminado__solicitud__subproyecto__nombre', lookup_expr='icontains')
    start_date = DateFilter(field_name='producto_terminado__solicitud__created_at', lookup_expr='gte')
    end_date = DateFilter(field_name='producto_terminado__solicitud__created_at', lookup_expr='lte')
    class Meta:
        model = EntradaArticulo
        fields = ['producto_terminado']