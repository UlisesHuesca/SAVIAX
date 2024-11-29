import django_filters
from .models import Activo, Estatus_Activo
from dashboard.models import Familia
from django_filters import CharFilter, DateTimeFilter, BooleanFilter, ModelChoiceFilter
from django.db.models import Q

class ActivoFilter(django_filters.FilterSet):
    eco_unidad = CharFilter(field_name='eco_unidad', lookup_expr='icontains')
    responsable = CharFilter(method ='my_filter', label="Search")
    tipo_activo = CharFilter(field_name='tipo_activo__nombre', lookup_expr='icontains')
    estatus = ModelChoiceFilter(queryset=Estatus_Activo.objects.all())
    familia = django_filters.ModelChoiceFilter(queryset=Familia.objects.filter(nombre__in=['ACTIVO', 'ACTIVO MENOR']),field_name='activo__producto__familia',
        label="Familia",empty_label="Todas las familias")
    subfamilia = CharFilter(field_name='activo__producto__subfamilia__nombre', lookup_expr='icontains')
    #subfamilia = CharFilter(field_name='subfamilia__nombre', lookup_expr='icontains')
    #distrito = CharFilter(field_name='responsable__distritos__nombre', lookup_expr='icontains')
    #activo = BooleanFilter()

    class Meta:
        model = Activo
        fields = ['eco_unidad','tipo_activo','activo','subfamilia']

    def my_filter(self, queryset, name, value):
        return queryset.filter(Q(responsable__staff__first_name__icontains = value) | Q(responsable__staff__last_name__icontains = value))