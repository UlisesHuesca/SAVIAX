from django import forms
from requisiciones.models import Salidas, ArticulosRequisitados

class SalidasForm(forms.ModelForm):
    class Meta:
        model = Salidas
        fields = ['cantidad','material_recibido_por']

class ArticulosRequisitadosForm(forms.ModelForm):
    class Meta:
        model = ArticulosRequisitados
        fields = ['cantidad']