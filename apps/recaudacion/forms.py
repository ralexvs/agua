from django import forms 
from .models import Recaudacion, RecaudacionDetalle
from apps.catastro.models import Abonado
from apps.parametro.models import Pago, Descuento
from django.forms.models import modelformset_factory, inlineformset_factory

class RecaudacionForm(forms.ModelForm):

    fecha = forms.DateInput()
    abonado = forms.ModelChoiceField(
        queryset=Abonado.objects.filter(estado=True)
        .order_by('apellidos')
    )
    pago = forms.ModelChoiceField(
        queryset=Pago.objects.filter(estado=True)
        .order_by('descripcion')
    )
       
    class Meta:
        model = Recaudacion
        fields = ('fecha','abonado', 'pago', 'descripcion',
                  'pago', 'descuento', 'total_consumo',)
    
    def __init__(self, *args, **kwargs):
        super(RecaudacionForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['fecha'].widget.attrs['readonly'] = True
        self.fields['abonado'].empty_label = 'Seleccione abonado'
        self.fields['pago'].empty_label = 'Seleccione pago'


class RecaudacionDetalleForm(forms.ModelForm):
  
    class Meta:
        model = RecaudacionDetalle
        fields = ['lectura_detalle', 'catastro', 'lectura_anterior',
                  'lectura_actual', 'consumo', 'base', 'base_reserva', 'valor_consumo_maximo', 'valor_excedente', 'total']


    def __init__(self, *args, **kwargs):
        super(RecaudacionDetalleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_lectura_anterior(self):
        lectura_anterior = self.cleaned_data['lectura_anterior']
        if lectura_anterior == '':
            raise forms.ValidationError("Debe ingresar una lec.  anter valida")
        return lectura_anterior

    def clean_lectura_actual(self):
        lectura_actual = self.cleaned_data['lectura_actual']
        if lectura_actual == '':
            raise forms.ValidationError(
                "Debe ingresar un lectura_actual valido")
        return lectura_actual


RecaudacionDetalleFormSet = inlineformset_factory(
    Recaudacion, RecaudacionDetalle, form=RecaudacionDetalleForm, extra=4)
