from django import forms
from .models import Solicitud_Gasto, Articulo_Gasto
from tesoreria.models import Pago

class Solicitud_GastoForm(forms.ModelForm):
    class Meta:
        model = Solicitud_Gasto
        fields = ['proyecto','subproyecto','area','superintendente','tipo']

class Articulo_GastoForm(forms.ModelForm):
    class Meta:
        model = Articulo_Gasto
        fields = ['clase','producto','comentario','cantidad','precio_unitario','factura_pdf','factura_xml','otros_impuestos','impuestos_retenidos','entrada_salida_express']

class Articulo_Gasto_Edit_Form(forms.ModelForm):
    class Meta:
        model = Articulo_Gasto
        fields = ['cantidad','precio_unitario','otros_impuestos','impuestos_retenidos']



class Pago_Gasto_Form(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto','comprobante_pago','cuenta']