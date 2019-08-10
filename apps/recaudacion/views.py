from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.core.views import SinPrivilegios, VistaBaseCreate, VistaBaseUpdate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.http import HttpResponse
from django.db.models import Sum
from .forms import RecaudacionForm, RecaudacionDetalleForm
from .models import Recaudacion
from apps.catastro.models import Abonado, Catastro, LecturaDetalle

from django.utils import  timezone
# Create your views here.


class RecaudacionList(SinPrivilegios,ListView):
    permission_required = 'recaudacion.view_recaudacion'
    model = Recaudacion
    template_name = "recaudacion/recaudacion_list.html"


class LecturaDetalleList(SinPrivilegios, ListView):
    
    permission_required = 'catastro.view_lecturadetalle'
    ahora = timezone.now()
    model = LecturaDetalle
    template_name = "recaudacion/lectura_detalle_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(LecturaDetalleList,self).get_context_data(**kwargs)
        context.update({'ahora':self.ahora})
        return context



@login_required(login_url='login')
@permission_required('recaudacion.view_recaudacion', login_url='sin_privilegio')
def recaudacion(request, recaudacion_id=None, catastro_id=None):

    template_name = 'recaudacion/recaudacion_create.html'
    cat = Catastro.objects.filter(estado=True, suspender=False, pk=catastro_id).first()
    ahora = timezone.now()
    
    #tipo_lectura = TipoLectura.objects.filter(estado=True)
    form_recaudacion = {}
    contexto = {}

    if request.method == 'GET':

        form_recaudacion = RecaudacionForm()
        #Filtramos la información que visualizamos en pantalla
        enc = Recaudacion.objects.filter(pk=recaudacion_id).first()

        if enc:

            det = RecaudacionDetalle.objects.filter(recaudacion=enc)
            
            fecha = datetime.date.isoformat(enc.fecha)
            e = {
                'fecha': fecha,
                'abonado': enc.abonado,
                'descripcion': enc.descripcion,
                'pago': enc.pago,
                'descuento': enc.descuento,
                'total_consumo': enc.total_consumo,
                'total_base': enc.total_base,
                'total_base_reserva': enc.total_base_reserva,
                'total_excedente': enc.total_excedente,
                'total_consumo_maximo': enc.total_consumo_maximo,
                'subtotal': enc.subtotal,
                'total_descuento': enc.total_descuento,
                'total_general': enc.total_general,
            }
            #Rendirizamos el formulario con los campos que devuelve enc.
            form_recaudacion = RecaudacionForm(e)

        else:
            det = None

        lectura_detalle = LecturaDetalle.objects.filter(
            estado=True, catastro=catastro_id)
        contexto = {'catastro': cat, 'encabezado': enc, 'detalle': det,
                    'form_enc': form_recaudacion, 'lectura_detalle': lectura_detalle, 'ahora':ahora}

    if request.method == 'POST':
        
        fecha= request.POST.get('fecha')
        abonado = request.POST.get('abonado')
        descripcion = request.POST.get('descripcion')
        pago = request.POST.get('pago')
        descuento = request.POST.get('descuento')
        total_consumo = 0
        total_base= 0
        total_base_reserva = 0
        total_excedente = 0
        total_consumo_maximo = 0
        subtotal: enc.subtotal= 0
        total_descuento = 0
        total_general = 0

        #si no se envia lectura_id quiere decir que el encabezado no existe
        if not recaudacion_id:
            #prov = Proveedor.objects.get(pk=proveedor)
            enc = Recaudacion(
                fecha=fecha,
                abonado=abonado,
                descripcion=descripcion,
                pago=pago,
                descuento=descuento,
                uc=request.user
            )
            if enc:
                enc.save()  # grava encabezado nuevo
                recaudacion_id = enc.id
        else:  # Editar encabezado
            enc = Recaudacion.objects.filter(pk=recaudacion_id).first()
            if enc:
                enc.fecha = fecha
                enc.abonado = abonado
                enc.descripcion = descripcion
                enc.pago = pago
                enc.um = request.user.id
                enc.save()

        if not recaudacion_id:
            return redirect('recaudacion:lectura_detalle_list')

        catastro = request.POST.get("catastro")
        lectura_anterior = request.POST.get("lectura_anterior")
        lectura_actual = request.POST.get("lectura_actual")
        consumo = request.POST.get("consumo")
        tl = request.POST.get('tipo_lectura')
        tipo = TipoLectura.objects.filter(pk=tl).first()
        tarifa = Tarifa.objects.filter(estado=True)

        for tar in tarifa:
            if int(consumo) >= tar.rango_inicial and int(consumo) <= tar.rango_superior:
                tarifa = tar
                excedente = tar.valor_excedente
                rango_inicial = tar.rango_inicial
            elif int(consumo) > tar.rango_superior:
                tarifa = tar
                excedente = tar.valor_excedente
                rango_inicial = tar.rango_inicial

        catas = Catastro.objects.filter(pk=catastro).first()
        base = catas.servicio.base
        base_reserva = catas.servicio.base_reserva

        if int(consumo) > catas.servicio.base_consumo:
            metros_excedidos = int(consumo) - rango_inicial
            valor_excedente = metros_excedidos * excedente
        else:
            valor_excedente = 0

        if int(consumo) >= catas.servicio.consumo_maximo:
            valor_consumo_maximo = catas.servicio.valor_consumo_maximo
        else:
            valor_consumo_maximo = 0

        det = LecturaDetalle(
            lectura=enc,
            catastro=catas,
            lectura_anterior=lectura_anterior,
            lectura_actual=lectura_actual,
            tarifa=tarifa,
            valor_excedente=valor_excedente,
            base=base,
            base_reserva=base_reserva,
            valor_consumo_maximo=valor_consumo_maximo,
            tipo_lectura=tipo,
            uc=request.user

        )
        if det:
            det.save()

            consumo_total = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('consumo'))
            total_base = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('base'))
            total_base_reserva = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('base_reserva'))
            total_excedente = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('valor_excedente'))
            total_consumo_maximo = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('valor_consumo_maximo'))
            total_general = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('total'))

            enc.consumo_total = consumo_total['consumo__sum']
            enc.total_base = total_base['base__sum']
            enc.total_base_reserva = total_base_reserva['base_reserva__sum']
            enc.total_excedente = total_excedente['valor_excedente__sum']
            enc.total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
            enc.total_general = total_general['total__sum']
            enc.save()

        return redirect('recaudacion:recaudacion_update', recaudacion_id=recaudacion_id) 
    
    return render(request, template_name, contexto)


class RecaudacionCreate(VistaBaseCreate, SinPrivilegios):
    permission_required = 'recaudacion.add_recaudacion'
    model = Recaudacion
    template_name = "recaudacion/recaudacion_create.html"
    form_class = RecaudacionDetalleForm
    success_url = reverse_lazy('recaudacion:recaucacion_list_r')

