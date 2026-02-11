from django import forms
from .models import Solicitud_Gasto, Articulo_Gasto, Entrada_Gasto_Ajuste, Conceptos_Entradas, Factura
from tesoreria.models import Pago
from solicitudes.models import Subproyecto, Proyecto
from dashboard.models import Inventario, Product


class Solicitud_GastoForm(forms.ModelForm):
    class Meta:
        model = Solicitud_Gasto
        fields = ['superintendente','colaborador','tipo']

class Articulo_GastoForm(forms.ModelForm):

    class Meta:
        model = Articulo_Gasto
        fields = ['producto','comentario','proyecto','subproyecto','cantidad','precio_unitario','factura_pdf','factura_xml','otros_impuestos','impuestos_retenidos']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proyecto'].queryset = Proyecto.objects.none()
        self.fields['subproyecto'].queryset = Subproyecto.objects.none()
        self.fields['producto'].queryset = Product.objects.none()

        if 'proyecto' in self.data:
            try:
                seleccion_actual = int(self.data.get('proyecto'))
                # Lógica para determinar el nuevo queryset basado en la selección actual
                self.fields['subproyecto'].queryset = Subproyecto.objects.filter(proyecto= seleccion_actual)  
                self.fields['proyecto'].queryset = Proyecto.objects.filter(id= seleccion_actual)
                        
            except (ValueError, TypeError):
                pass  # Manejo de errores en caso de entrada no válida
        if 'producto' in self.data:
            try:
                seleccion_actual = int(self.data.get('producto'))
                # Lógica para determinar el nuevo queryset basado en la selección actual
                self.fields['producto'].queryset = Inventario.objects.filter(id= seleccion_actual)
            except (ValueError, TypeError):
                pass  # Manejo de errores en caso de entrada no válida
    
class Articulo_GastoForm2(forms.ModelForm):

    class Meta:
        model = Articulo_Gasto
        fields = ['producto','factura_xml','comentario']


class Articulo_Gasto_Edit_Form(forms.ModelForm):
    class Meta:
        model = Articulo_Gasto
        fields = ['cantidad','precio_unitario','otros_impuestos','impuestos_retenidos']


class Pago_Gasto_Form(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto','comprobante_pago','cuenta', 'pagado_real',]

class Articulo_Gasto_Factura_Form(forms.ModelForm):

    class Meta:
        model = Articulo_Gasto
        fields = ['factura_pdf','factura_xml']

class Entrada_Gasto_AjusteForm(forms.ModelForm):
    
    class Meta:
        model = Entrada_Gasto_Ajuste
        fields = ['comentario']

class Conceptos_EntradasForm(forms.ModelForm):

    class Meta:
        model = Conceptos_Entradas
        fields =['concepto_material','cantidad','precio_unitario','comentario']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['archivo_pdf', 'archivo_xml']

class Autorizacion_Gasto_Form(forms.ModelForm):
    class Meta:
        model = Solicitud_Gasto
        fields = ['comentarios']