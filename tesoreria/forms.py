from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto','comprobante_pago','tipo_de_cambio','cuenta']
