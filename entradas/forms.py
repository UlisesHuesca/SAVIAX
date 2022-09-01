from django import forms
from .models import Entrada, EntradaArticulo

class EntradaArticuloForm(forms.ModelForm):
    class Meta:
        model = EntradaArticulo
        fields = ['cantidad']
