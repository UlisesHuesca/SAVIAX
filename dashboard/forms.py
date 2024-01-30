from django import forms
from .models import Product, Subfamilia, Products_Batch, Inventario_Batch, Familia, Producto_Calidad
from compras.models import Proveedor_Batch, Proveedor, Proveedor_direcciones, Proveedor_Direcciones_Batch
from solicitudes.models import Proyecto, Subproyecto


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['familia','subfamilia','unidad','especialista','iva','activo','servicio','baja_item','image','gasto','critico','especs']

    #Sobreescribiendo el método __init__ y configurando el queryset para que esté vacío
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['familia'].queryset = Familia.objects.none()
        self.fields['subfamilia'].queryset = Subfamilia.objects.none()

        if 'familia' in self.data:
            try:
                familia_id = int(self.data.get('familia'))
                self.fields['subfamilia'].queryset = Subproyecto.objects.filter(familia = familia_id)  
                self.fields['familia'].queryset = Proyecto.objects.filter(id= familia_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

class AddProduct_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['codigo','nombre','unidad','familia','subfamilia','especialista','iva','activo','servicio','image','gasto','critico','especs']

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

#class ProductEditCalidad_Form(forms.ModelForm):
#    class Meta:
#        model = Product
#        fields = ['nombre','unidad','critico']

class Revision_Calidad_Form(forms.ModelForm):
    class Meta:
        model = Producto_Calidad
        fields = ['requisitos', 'documental', 'inspeccion', 'cumplimiento','g_documental','g_inspeccion','g_cumplimiento']

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social','rfc','nombre_comercial','familia']

class DireccionComparativoForm(forms.ModelForm):
   
    class Meta:
        model = Proveedor_direcciones
        fields = ['email']

class ProveedoresDireccionesForm(forms.ModelForm):
    class Meta:
        model = Proveedor_direcciones
        fields = ['estado','domicilio','contacto','telefono','email','email_opt','banco','swift','clabe','cuenta','financiamiento','dias_credito','estatus']

class ProveedoresExistDireccionesForm(forms.ModelForm):
   
    class Meta:
        model = Proveedor_direcciones
        fields = ['nombre','domicilio','estado','contacto','telefono','email','email_opt','banco','clabe','cuenta','financiamiento','dias_credito']


class Add_ProveedoresDireccionesForm(forms.ModelForm):
    class Meta:
        model = Proveedor_direcciones
        fields = ['domicilio','estado','contacto','email','email_opt','telefono','banco','swift','clabe','cuenta','financiamiento','dias_credito','estatus']

class Products_BatchForm(forms.ModelForm):
    class Meta:
        model = Products_Batch
        fields= ['file_name']

class Inventario_BatchForm(forms.ModelForm):
    class Meta:
        model = Inventario_Batch
        fields= ['file_name']

class Proveedores_BatchForm(forms.ModelForm):
    class Meta:
        model = Proveedor_Batch
        fields= ['file_name']

class Proveedores_Direcciones_BatchForm(forms.ModelForm):
    class Meta:
        model = Proveedor_Direcciones_Batch
        fields= ['file_name']



class Proyectos_Form(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['descripcion','nombre','cliente','activo','factura','fecha_factura','folio_cotizacion','oc_cliente','status_de_entrega',]

class Proyectos_Add_Form(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['descripcion','nombre','cliente','factura','fecha_factura','folio_cotizacion','oc_cliente','status_de_entrega',]

class Subproyectos_Add_Form(forms.ModelForm):
    class Meta:
        model = Subproyecto
        fields = ['nombre','descripcion','presupuesto']