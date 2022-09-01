from django import forms
from solicitudes.models import Subproyecto, Proyecto
from dashboard.models import Inventario, Order, Product, ArticulosOrdenados

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto','marca','cantidad', 'price']

    def __init__(self, *args, **kwargs):

        #item_creado = Inventario.objects.get(complete=False)


        super(InventarioForm, self).__init__(*args, **kwargs)
        #distrito = kwargs.pop('distrito')
        # Get a 'value list' of products already in the inventario model
        #existing = Inventario.objects.filter(distrito=item_creado.distrito).values_list('producto')
        existing = Inventario.objects.all().values_list('producto')

        # Override the product query set with a list of product excluding those already in the pricelist
        self.fields['producto'].queryset = Product.objects.exclude(id__in=existing)

class ArticulosOrdenadosForm(forms.ModelForm):

    class Meta:
        model = ArticulosOrdenados
        fields = ['cantidad']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['proyecto','subproyecto', 'operacion','activo']

#Sobreescribiendo el método __init__ y configurando el queryset para que esté vacío
    def __init__(self, *args, **kwargs):
        distrito = kwargs.pop('distrito')
        super().__init__(*args, **kwargs)
        self.fields['subproyecto'].queryset = Subproyecto.objects.none()
        self.fields['proyecto'].queryset = Proyecto.objects.filter(distrito=distrito)

        if 'proyecto' in self.data:
            try:
                proyecto_id = int(self.data.get('proyecto'))
                self.fields['subproyecto'].queryset = Subproyecto.objects.filter(proyecto_id=proyecto_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty subproyecto queryset
        #elif self.instance.pk:
        #    self.fields['subproyecto'].queryset = self.instance.proyecto.subproyecto_set.order_by('nombre')

class Inv_UpdateForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['marca','cantidad','cantidad_apartada', 'price','comentario','minimo']
