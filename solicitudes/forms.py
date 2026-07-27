from django import forms
from django.db.models import Q 
from solicitudes.models import Subproyecto, Proyecto
from dashboard.models import Inventario, Order, Product, ArticulosOrdenados, Plantilla, ArticuloPlantilla
from gastos.models import Entrada_Gasto_Ajuste, Conceptos_Entradas 

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto','cantidad', 'price','comentario']

    def __init__(self, *args, **kwargs):

        #item_creado = Inventario.objects.get(complete=False)


        super(InventarioForm, self).__init__(*args, **kwargs)
        #distrito = kwargs.pop('distrito')
        # Get a 'value list' of products already in the inventario model
        #existing = Inventario.objects.filter(distrito=item_creado.distrito).values_list('producto')
        existing = Inventario.objects.all().values_list('producto')

        # Override the product query set with a list of product excluding those already in the pricelist
        self.fields['producto'].queryset = Product.objects.filter().exclude(id__in=existing)

class ArticulosOrdenadosForm(forms.ModelForm):

    class Meta:
        model = ArticulosOrdenados
        fields = ['cantidad']

class ArticulosOrdenadosComentForm(forms.ModelForm):

    class Meta:
        model = ArticulosOrdenados
        fields = ['comentario']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['proyecto','subproyecto', 'area','superintendente','supervisor','comentario','soporte']

    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
        #usuario_distrito = getattr(self.instance, 'distrito', None)
         # Modificar la etiqueta de "Superintendente" a "Gerente" si el distrito es BRASIL
        #if usuario_distrito == "BRASIL":
        #    self.fields['superintendente'].label = _("Gerente*")


        self.fields['proyecto'].queryset = Proyecto.objects.none()
        self.fields['subproyecto'].queryset = Subproyecto.objects.none()

        if 'proyecto' in self.data:
            try:
                seleccion_actual = int(self.data.get('proyecto'))
                # Lógica para determinar el nuevo queryset basado en la selección actual
                self.fields['subproyecto'].queryset = Subproyecto.objects.filter(proyecto= seleccion_actual)  
                self.fields['proyecto'].queryset = Proyecto.objects.filter(id= seleccion_actual)
                        
            except (ValueError, TypeError):
                pass  # Manejo de errores en caso de entrada no válida
        
class Order_Resurtimiento_Form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['proyecto','subproyecto','superintendente','comentario']

class Inv_UpdateForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['price','cantidad','minimo','ubicacion','estante','comentario']

class Inv_UpdateForm_almacenista(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['ubicacion','estante','minimo','comentario']

class Entrada_Gasto_AjusteForm(forms.ModelForm):
    class Meta:
        model = Entrada_Gasto_Ajuste
        fields = ['comentario']

class Conceptos_EntradasForm(forms.ModelForm):
    class Meta:
        model = Conceptos_Entradas
        fields = ['concepto_material','cantidad', 'precio_unitario']

class Plantilla_Form(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['nombre','descripcion','comentario']

class ArticuloPlantilla_Form(forms.ModelForm):
    class Meta:
        model = ArticuloPlantilla
        fields = ['producto','cantidad','comentario_articulo','comentario_plantilla']