from django import forms
from requisiciones.models import Salidas, ArticulosRequisitados, ValeSalidas

class SalidasForm(forms.ModelForm):
    class Meta:
        model = Salidas
        fields = ['producto','cantidad']

class ValeSalidasForm(forms.ModelForm):
    class Meta:
        model = ValeSalidas
        fields = ['material_recibido_por']

class ArticulosRequisitadosForm(forms.ModelForm):
    class Meta:
        model = ArticulosRequisitados
        fields = ['cantidad']