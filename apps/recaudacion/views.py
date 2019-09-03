from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.core.views import SinPrivilegios, VistaBaseCreate, VistaBaseUpdate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.db.models.functions import Round
from django.http import HttpResponse
from django.db.models import Sum
from .forms import RecaudacionForm, RecaudacionDetalleForm
from .models import Recaudacion, RecaudacionDetalle
from apps.catastro.models import Abonado, Catastro, LecturaDetalle

from django.utils import  timezone
# Create your views here.


class RecaudacionList(SinPrivilegios,ListView):
    permission_required = 'recaudacion.view_recaudacion'
    model = Recaudacion
    template_name = "recaudacion/recaudacion_list.html"


class LecturaDetalleList(SinPrivilegios, ListView):
    
    permission_required = 'catastro.view_lecturadetalle'
    model = LecturaDetalle
    template_name = "recaudacion/lectura_detalle_list.html"
    queryset = LecturaDetalle.objects.filter(estado=True)
    
    def get_context_data(self, **kwargs):
        context = super(LecturaDetalleList,self).get_context_data(**kwargs)
        #context.update({'ahora':self.ahora}) #tambien funciona
        context['ahora'] = timezone.now()
        return context



@login_required(login_url='login')
@permission_required('recaudacion.view_recaudacion', login_url='sin_privilegio')
def recaudacion(request, recaudacion_id=None, catastro_id=None):

    template_name = 'recaudacion/recaudacion_create.html'
    cat = Catastro.objects.filter(estado=True, suspender=False, pk=catastro_id).first()
    #ahora = timezone.now()
    ahora = datetime.date.isoformat(timezone.now())
    #tipo_lectura = TipoLectura.objects.filter(estado=True)
    form_recaudacion = {}
    contexto = {}
    total_consumo=0
    total_base=0
    total_base_reserva=0
    total_excedente=0
    total_consumo_maximo =0
    total_administracion = 0
    total_alcantarillado=0
    total_derecho_conexion = 0
    descuento = 0
    subtotal = 0
    total_descuento = 0
    total_general =0

    if request.method == 'GET':

        form_recaudacion = RecaudacionForm()
        #Filtramos la información que visualizamos en pantalla
        enc = Recaudacion.objects.filter(pk=recaudacion_id).first()
        
        det = None

        lectura_detalle = LecturaDetalle.objects.filter(
            estado=True, catastro=catastro_id)
        
        total_consumo = LecturaDetalle.objects.filter(
            catastro=catastro_id,estado=True).aggregate(Sum('consumo'))
        total_base = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('base'))
        total_base_reserva = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('base_reserva'))
        total_excedente = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('valor_excedente'))
        total_consumo_maximo = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('valor_consumo_maximo'))
        total_administracion = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('administracion'))
        total_alcantarillado = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('alcantarillado'))
        total_derecho_conexion = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('derecho_conexion'))
        total_general = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('total'))

        total_consumo = total_consumo['consumo__sum']
        total_base = total_base['base__sum']
        total_base_reserva = total_base_reserva['base_reserva__sum']
        total_excedente = total_excedente['valor_excedente__sum']
        total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
        total_administracion = total_administracion['administracion__sum']
        total_alcantarillado = total_alcantarillado['alcantarillado__sum']
        total_derecho_conexion = total_derecho_conexion['derecho_conexion__sum']
        subtotal = total_base + total_base_reserva+total_excedente + \
            total_consumo_maximo + total_administracion + \
            total_alcantarillado+total_derecho_conexion
        valor = cat.descuento.valor
        if valor > 0:
            total_descuento = (subtotal * valor)/100
        
        
        total_general = total_general['total__sum'] - round(total_descuento, 2)

        contexto = {'catastro': cat,
            'encabezado': enc,
            'detalle': det,
            'form_enc': form_recaudacion, 
            'lectura_detalle': lectura_detalle, 
            'ahora': ahora,
                    'total_consumo': total_consumo,
                    'total_base': total_base,
                    'total_base_reserva': total_base_reserva,
                    'total_excedente': total_excedente,
                    'total_consumo_maximo': total_consumo_maximo,
                    'total_administracion' : total_administracion,
                    'total_alcantarillado' : total_alcantarillado,
                    'total_derecho_conexion' : total_derecho_conexion,
                    'subtotal': subtotal,
                    'total_descuento': round(total_descuento, 2),
                    'total_general': total_general,
        }
    if request.method == 'POST':
        
        fecha= request.POST.get('fecha')
        abonado = cat.abonado
        descripcion = request.POST.get('descripcion')
        pago = cat.pago
        descuento = cat.descuento
        total_consumo = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('consumo'))
        total_base = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('base'))
        total_base_reserva = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('base_reserva'))
        total_excedente = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('valor_excedente'))
        total_consumo_maximo = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('valor_consumo_maximo'))
        total_administracion = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('administracion'))
        total_alcantarillado = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('alcantarillado'))
        total_derecho_conexion = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('derecho_conexion'))
        total_general = LecturaDetalle.objects.filter(
            catastro=catastro_id, estado=True).aggregate(Sum('total'))

        total_consumo = total_consumo['consumo__sum']
        total_base = total_base['base__sum']
        total_base_reserva = total_base_reserva['base_reserva__sum']
        total_excedente = total_excedente['valor_excedente__sum']
        total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
        total_administracion = total_administracion['administracion__sum']
        total_alcantarillado = total_alcantarillado['alcantarillado__sum']
        total_derecho_conexion = total_derecho_conexion['derecho_conexion__sum']
        subtotal = total_base + total_base_reserva+total_excedente+total_consumo_maximo + total_administracion + total_alcantarillado+total_derecho_conexion
        valor = cat.descuento.valor
        if valor > 0:
            total_descuento = (subtotal * valor)/100


        #si no se envia recaudacion_id quiere decir que el encabezado no existe
        if not recaudacion_id:
            #prov = Proveedor.objects.get(pk=proveedor)
            enc = Recaudacion(
                fecha=fecha,
                abonado=abonado,
                descripcion=descripcion,
                pago=pago,
                descuento=descuento,
                total_consumo = total_consumo,
                total_base=total_base,
                total_base_reserva=total_base_reserva,
                total_excedente=total_excedente,
                total_consumo_maximo=total_consumo_maximo,
                total_administracion = total_administracion,
                total_alcantarillado = total_alcantarillado,
                total_derecho_conexion = total_derecho_conexion,
                #subtotal = subtotal,
                total_descuento = total_descuento,
                #total_general=total_general,
                uc=request.user
            )
            if enc:
                enc.save()  # grava encabezado nuevo
                recaudacion_id = enc.id
            
        #return redirect('recaudacion:recaudacion_detalle_list')
        detalle = LecturaDetalle.objects.filter(estado=True, catastro=catastro_id)
        enc = Recaudacion.objects.filter(pk=recaudacion_id).first()
        for deta in detalle:
            det = RecaudacionDetalle(
                recaudacion=enc,
                lectura=deta,
                numero=deta.catastro.numero,
                lectura_anterior=deta.lectura_anterior,
                lectura_actual=deta.lectura_actual,
                consumo=deta.consumo,
                base=deta.base,
                base_reserva=deta.base_reserva,
                valor_consumo_maximo=deta.valor_consumo_maximo,
                valor_excedente=deta.valor_excedente,
                administracion = deta.administracion,
                alcantarillado = deta.alcantarillado,
                derecho_conexion = deta.derecho_conexion,
                uc = request.user,
            )
            if det:
                det.save()
            
        return redirect('recaudacion:lectura_detalle_list')

    return render(request, template_name, contexto)


class RecaudacionCreate(VistaBaseCreate, SinPrivilegios):
    permission_required = 'recaudacion.add_recaudacion'
    model = Recaudacion
    template_name = "recaudacion/recaudacion_create.html"
    form_class = RecaudacionDetalleForm
    success_url = reverse_lazy('recaudacion:recaucacion_list_r')

def plantilla(request, id=None, doc=None):
    model = RecaudacionDetalle.objects.all()
    template_name = 'recaudacion/reportes/planilla.html'
    context = {'model':model}
    return render(request, template_name, context)


