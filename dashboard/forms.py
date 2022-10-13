from django import forms
from .models import Product, Subfamilia, Products_Batch, Inventario_Batch


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['familia','subfamilia','unidad','especialista','iva','activo','servicio','baja_item','image',]

#Sobreescribiendo el método __init__ y configurando el queryset para que esté vacío
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subfamilia'].queryset = Subfamilia.objects.none()

        if 'familia' in self.data:
            try:
                familia_id = int(self.data.get('familia'))
                self.fields['subfamilia'].queryset = Subfamilia.objects.filter(familia_id=familia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subfamilia'].queryset = self.instance.familia.subfamilia_set.order_by('nombre')

class Products_BatchForm(forms.ModelForm):
    class Meta:
        model = Products_Batch
        fields= ['file_name']

class Inventario_BatchForm(forms.ModelForm):
    class Meta:
        model = Inventario_Batch
        fields= ['file_name']

class AddProduct_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['codigo','nombre','unidad','familia','subfamilia','especialista','iva','activo','servicio','image',]

#Sobreescribiendo el método __init__ y configurando el queryset para que esté vacío
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subfamilia'].queryset = Subfamilia.objects.none()

        if 'familia' in self.data:
            try:
                familia_id = int(self.data.get('familia'))
                self.fields['subfamilia'].queryset = Subfamilia.objects.filter(familia_id=familia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subfamilia'].queryset = self.instance.familia.subfamilia_set.order_by('nombre')
