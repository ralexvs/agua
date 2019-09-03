from django import forms 
from .models import Entidad, Servicio, Tarifa, Multa, Descuento, Pago


class EntidadForm(forms.ModelForm):
  
    class Meta:
        model = Entidad
        fields = (
            'ruc', 
            'descripcion', 
            'direccion', 
            'telefono',
            'celular',
            'correo',
            'web',
            'estado',
            'logo',
        )
        widget = {'descripcion': forms.TextInput}
        
    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if field != 'logo':
                self.fields[field].widget.attrs.update({'class':'form-control'})


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = (
            'descripcion',
            'base',
            'base_reserva',
            'base_consumo',
            'consumo_maximo',
            'valor_consumo_maximo',
            'administracion',
            'alcantarillado',
            'derecho_conexion',
            'derecho_conexion_nuevo_comunidad',
            'estado',
        )
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})


class TarifaForm(forms.ModelForm):
     
    class Meta:
        model = Tarifa
        fields = (
            'descripcion',
            'rango_inicial',
            'rango_superior',
            'valor_excedente',
            'estado',
        )
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super(TarifaForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})
        


class MultaForm(forms.ModelForm):

    class Meta:
        model = Multa
        fields = (
            'descripcion',
            'valor',
            'estado',
        )
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super(MultaForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})

class DescuentoForm(forms.ModelForm):
    
    class Meta:
        model = Descuento
        fields = (
            'descripcion',
            'valor',
            'estado',
        )
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super(DescuentoForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})


class PagoForm(forms.ModelForm):

    class Meta:
        model = Pago
        fields = (
            'descripcion',
            'estado',
        )
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'})
