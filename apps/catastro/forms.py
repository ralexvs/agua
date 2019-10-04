from django import forms 
from .models import Medidor, Barrio, Abonado, Medidor, Catastro, TipoLectura, Lectura, LecturaDetalle, MultaDetalle
from apps.parametro.models import Pago, Servicio, Descuento, Multa


class MedidorForm(forms.ModelForm):
    
    class Meta:
        
        model = Medidor
        fields = ('numero', 'descripcion', 'modelo','lectura_inicial','estado')
        widget = {'descripcion': forms.TextInput}
        exclude = ('asignar',)
    
    def __init__(self, *args, **kwargs):

        super(MedidorForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({'class':'form-control'})


class BarrioForm(forms.ModelForm):

    class Meta:

        model = Barrio
        fields = ('descripcion', 'estado')
        widget = {'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):

        super(BarrioForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AbonadoForm(forms.ModelForm):
    
    barrio = forms.ModelChoiceField(
        queryset=Barrio.objects.filter(estado=True)
        .order_by('descripcion')
    )

    class Meta:

        model = Abonado
        fields = ('identificacion', 'apellidos', 'nombres', 'direccion',
                  'email', 'web', 'telefono', 'celular', 'fecha_nacimiento','sexo', 'barrio', 'estado', 'foto')

    def __init__(self, *args, **kwargs):

        super(AbonadoForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['barrio'].empty_label = 'Seleccione barrio o sector'
        self.fields['sexo'].widget.attrs['readonly'] = True
        self.fields['fecha_nacimiento'].widget.attrs['readonly'] = True



class CatastroForm(forms.ModelForm):

    abonado = forms.ModelChoiceField(
        queryset=Abonado.objects.filter(estado=True)
        .order_by('apellidos')
    )
    medidor = forms.ModelChoiceField(
        queryset=Medidor.objects.filter(estado=True)
        .order_by('descripcion')
    )

    class Meta:

        model = Catastro
        fields = ('numero', 'abonado',  'estado', 'fecha', 'peticionario', 'servicio', 'suspender', 'pago',
                   'medidor', 'descuento', 'descripcion',    'alcantarillado')
        #exclude = ('suspender',)
        
        labels = {'estado':'Activo',}
        widget = {'fecha': forms.TextInput}


    def __init__(self, *args, **kwargs):

        super(CatastroForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['abonado'].empty_label = 'Seleccione abonado'
        self.fields['servicio'].empty_label = 'Seleccione servicio'
        self.fields['pago'].empty_label = 'Seleccione pago'
        self.fields['medidor'].empty_label = 'Seleccione medidor'
        self.fields['descuento'].empty_label = 'Seleccione tipo descuento'
        self.fields['fecha'].widget.attrs['readonly'] = True


class TipoLecturaForm(forms.ModelForm):
    
    class Meta:
        
        model = TipoLectura
        fields = ('descripcion','estado')

    def __init__(self, *args, **kwargs):
        
        super(TipoLecturaForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):

            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LecturaForm(forms.ModelForm):
    #Renderizamos la fecha con forms.DateInput
    #periodo = forms.DateField(input_formats=['%b/%Y'])

    
    class Meta:
        model = Lectura
        fields = ('periodo', 'descripcion', 'consumo_total',
                'total_base', 'total_base_reserva', 'total_excedente', 'total_consumo_maximo', 'total_administracion',
                  'total_alcantarillado', 'total_derecho_conexion','total_otros', 'total_general')
    
    def __init__(self, *args, **kwargs):

        super(LecturaForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        
        self.fields['periodo'].widget.attrs['readonly']=True
        self.fields['consumo_total'].widget.attrs['readonly'] = True
        self.fields['total_base'].widget.attrs['readonly'] = True
        self.fields['total_base_reserva'].widget.attrs['readonly'] = True
        self.fields['total_excedente'].widget.attrs['readonly'] = True
        self.fields['total_consumo_maximo'].widget.attrs['readonly'] = True
        self.fields['total_administracion'].widget.attrs['readonly'] = True
        self.fields['total_alcantarillado'].widget.attrs['readonly'] = True
        self.fields['total_derecho_conexion'].widget.attrs['readonly'] = True
        self.fields['total_otros'].widget.attrs['readonly'] = True
        self.fields['total_general'].widget.attrs['readonly'] = True

class MultaDetalleForm(forms.ModelForm):
    
    lectura = forms.ModelChoiceField(queryset=LecturaDetalle.objects.filter(estado=False).order_by('id'))
    multa = forms.ModelChoiceField(queryset=Multa.objects.filter(estado=True).order_by('descripcion'))
    
    class Meta:
        model = MultaDetalle
        fields = ('lectura_detalle','multa','cantidad','valor','total')
        
    def __init__(self, *args, **kwargs):
        super(MultaDetalleForm, self).__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({ 'class':'form-control'})


    
