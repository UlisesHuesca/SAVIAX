import django_filters
from .models import Product
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')
    codigo = CharFilter(field_name='codigo', lookup_expr='icontains')
    familia = CharFilter(field_name='familia__nombre', lookup_expr='icontains')
    subfamilia = CharFilter(field_name='subfamilia__nombre', lookup_expr='icontains')



    class Meta:
        model = Product
        fields = ['codigo','nombre','familia', 'subfamilia',]