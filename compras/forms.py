from django import forms
from .models import Compra, ArticuloComprado, Comparativo, Item_Comparativo, Preevaluacion, Proveedor_direcciones, Proveedor
from requisiciones.models import ArticulosRequisitados

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['id','proveedor','cond_de_pago','uso_del_cfdi','dias_de_credito','deposito_comprador','anticipo',
                  'monto_anticipo','dias_de_entrega','impuesto','impuestos_adicionales','flete','costo_fletes',
                  'tesoreria_matriz','opciones_condiciones','moneda','tipo_de_cambio','logistica', 'referencia','comparativo_model']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor_direcciones.objects.none()
        self.fields['comparativo_model'].queryset = Comparativo.objects.none()
        if 'proveedor' in self.data:
            try:
                seleccion_actual = int(self.data.get('proveedor'))
                # Lógica para determinar el nuevo queryset basado en la selección actual
                self.fields['proveedor'].queryset = Proveedor_direcciones.objects.filter(id= seleccion_actual)
            except (ValueError, TypeError):
                pass  # Manejo de errores en caso de entrada no válida
        if 'comparativo_model' in self.data:
            try:
                seleccion_actual = int(self.data.get('comparativo_model'))
                self.fields['comparativo_model'].queryset = Comparativo.objects.filter(id = seleccion_actual)
            except (ValueError, TypeError):
                pass #Manejo de errores en caso de entrada no válida

class ArticuloCompradoForm(forms.ModelForm):
    class Meta:
        model = ArticuloComprado
        fields = ['producto','cantidad','precio_unitario']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = ArticulosRequisitados.objects.none() 
    

class ArticulosRequisitadosForm(forms.ModelForm):

    class Meta:
        model = ArticulosRequisitados
        fields = ['producto','cantidad']

class ComparativoForm(forms.ModelForm):
    class Meta:
        model = Comparativo
        fields = ['nombre','comentarios','proveedor', 'proveedor2','proveedor3','cotizacion','cotizacion2', 'cotizacion3']

class Item_ComparativoForm(forms.ModelForm):
    class Meta:
        model = Item_Comparativo
        fields = ['producto','modelo','marca','cantidad', 'precio','dias_de_entrega', 'modelo2', 'marca2','dias_de_entrega2', 
                  'precio2','modelo3','marca3','precio3','dias_de_entrega3',]

class Compra_ComentarioForm(forms.ModelForm):
    especs_b = forms.BooleanField(required=False)
    precios_b = forms.BooleanField(required=False)
    control_cadena_b = forms.BooleanField(required=False)
    capacidad_proveedor_b = forms.BooleanField(required=False)
    sgc_b = forms.BooleanField(required=False)

    class Meta:
        model = Compra
        fields = ['comentarios']

class PreevaluacionForm(forms.ModelForm):
    class Meta:
        model = Preevaluacion
        fields = ['tipo_evaluacion','comparativo_model','especs_ver','especs_b','precios_ver','precios_b','control_cadena_suministro',
                  'control_cadena_b','capacidad_proveedor','capacidad_proveedor_b','requisitos_sgc_ver','sgc_b']


class Compra_Comment_Form(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['comentarios']