from django import forms
from .models import Solicitud_Viatico, Concepto_Viatico, Viaticos_Factura
from solicitudes.models import Subproyecto, Proyecto
from tesoreria.models import Pago


class Solicitud_ViaticoForm(forms.ModelForm):
    class Meta:
        model = Solicitud_Viatico
        fields = ['proyecto','subproyecto','superintendente','fecha_partida','fecha_retorno','colaborador','lugar_partida','lugar_comision','hospedaje','transporte','comentario']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
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

class Concepto_ViaticoForm(forms.ModelForm):

    class Meta:
        model = Concepto_Viatico
        fields = ['producto','comentario','cantidad','precio','rendimiento','viatico']

class Pago_Viatico_Form(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto','comprobante_pago','cuenta']

class Viaticos_Factura_Form(forms.ModelForm):
    class Meta:
        model = Viaticos_Factura
        fields = ['factura_pdf','factura_xml','comentario']

class Cancelacion_viatico_Form(forms.ModelForm):
    class Meta:
        model = Solicitud_Viatico
        fields = ['comentarios_cancelacion']