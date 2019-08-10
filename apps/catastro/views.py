from django.shortcuts import render, redirect
from .models import Medidor, Barrio, Abonado, Catastro, TipoLectura, Lectura, LecturaDetalle
from apps.parametro.models import Tarifa, Multa, Pago
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from apps.core.views import SinPrivilegios, VistaBaseCreate, VistaBaseUpdate
from django.urls import reverse_lazy
from .forms import MedidorForm, BarrioForm, AbonadoForm, CatastroForm, TipoLecturaForm, LecturaForm
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Sum, Q, Max
from django.shortcuts import get_object_or_404


# Create your views here.



#CRUD Medidor =======================================================


class MedidorList(SinPrivilegios, ListView):

    permission_required = 'catastro.view_medidor'
    model = Medidor


class MedidorCreate(VistaBaseCreate):

    permission_required = 'catastro.add_medidor'
    model = Medidor
    template_name = "catastro/medidor_form.html"
    form_class = MedidorForm
    success_url = reverse_lazy('catastro:medidor_list')


class MedidorUpdate(VistaBaseUpdate):

    permission_required = 'catastro.change_medidor'
    model = Medidor
    template_name = "catastro/medidor_form.html"
    form_class = MedidorForm
    success_url = reverse_lazy('catastro:medidor_list')


class MedidorDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_medidor'
    model = Medidor
    template_name = "catastro/medidor_del.html"
    success_url = reverse_lazy('catastro:medidor_list')


@login_required(login_url='login')
@permission_required('catastro.change_medidor', login_url='sin_privilegio')
def medidor_inactivar(request, id):

    medidor = Medidor.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/medidor_inactivar.html'

    if not medidor:

        return redirect('catastro:medidor_list')

    if request.method == 'GET':

        contexto = {'object': medidor}

    if request.method == 'POST':

        medidor.estado = False
        medidor.save()
        return redirect('catastro:medidor_list')

    return render(request, template_name, contexto)



#CRUD Barrio =======================================================

class BarrioList(SinPrivilegios, ListView):

    permission_required = 'catastro.view_barrio'
    model = Barrio


class BarrioCreate(VistaBaseCreate):

    permission_required = 'catastro.add_barrio'
    model = Barrio
    template_name = "catastro/barrio_form.html"
    form_class = BarrioForm
    success_url = reverse_lazy('catastro:barrio_list')


class BarrioUpdate(VistaBaseUpdate):

    permission_required = 'catastro.change_barrio'
    model = Barrio
    template_name = "catastro/barrio_form.html"
    form_class = BarrioForm
    success_url = reverse_lazy('catastro:barrio_list')


class BarrioDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_barrio'
    model = Barrio
    template_name = "catastro/barrio_del.html"
    success_url = reverse_lazy('catastro:barrio_list')


@login_required(login_url='login')
@permission_required('catastro.change_barrio', login_url='sin_privilegio')
def barrio_inactivar(request, id):

    barrio = Barrio.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/barrio_inactivar.html'

    if not barrio:

        return redirect('catastro:barrio_list')

    if request.method == 'GET':

        contexto = {'object': barrio}

    if request.method == 'POST':

        barrio.estado = False
        barrio.save()
        return redirect('catastro:barrio_list')

    return render(request, template_name, contexto)


#CRUD Abonado =======================================================
class AbonadoList(SinPrivilegios, ListView):

    permission_required = 'catastro.view_abonado'
    model = Abonado


class AbonadoCreate(VistaBaseCreate):

    permission_required = 'catastro.add_abonado'
    model = Abonado
    template_name = "catastro/abonado_form.html"
    form_class = AbonadoForm
    success_url = reverse_lazy('catastro:abonado_list')


class AbonadoUpdate(VistaBaseUpdate):

    permission_required = 'catastro.change_abonado'
    model = Abonado
    template_name = "catastro/abonado_form.html"
    form_class = AbonadoForm
    success_url = reverse_lazy('catastro:abonado_list')


class AbonadoDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_abonado'
    model = Abonado
    template_name = "catastro/abonado_del.html"
    success_url = reverse_lazy('catastro:abonado_list')


@login_required(login_url='login')
@permission_required('catastro.change_abonado', login_url='sin_privilegio')
def abonado_inactivar(request, id):

    abonado = Abonado.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/abonado_inactivar.html'

    if not abonado:

        return redirect('catastro:abonado_list')

    if request.method == 'GET':

        contexto = {'object': abonado}

    if request.method == 'POST':

        abonado.estado = False
        abonado.save()
        return redirect('catastro:abonado_list')

    return render(request, template_name, contexto)


@login_required(login_url='login')
@permission_required('catastro.change_abonado', login_url='sin_privilegio')
def abonado_inactivar_js(request, id):
    abonado = Abonado.objects.filter(pk=id).first()

    if request.method=='POST':
        if abonado:
            abonado.estado = not abonado.estado
            abonado.save()
            return HttpResponse('OK')
        return HttpResponse('FATAL')

    return HttpResponse('FATAL')


#CRUD Catastro =======================================================

class CatastroList(SinPrivilegios, ListView):

    permission_required = 'catastro.view_catastro'
    model = Catastro


class CatastroCreate(VistaBaseCreate):

    permission_required = 'catastro.add_catastro'
    model = Catastro
    template_name = "catastro/catastro_form.html"
    form_class = CatastroForm
    success_url = reverse_lazy('catastro:catastro_list')


class CatastroUpdate(VistaBaseUpdate):

    permission_required = 'catastro.change_catastro'
    model = Catastro
    template_name = "catastro/catastro_form.html"
    form_class = CatastroForm
    success_url = reverse_lazy('catastro:catastro_list')


class CatastroDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_catastro'
    model = Catastro
    template_name = "catastro/catastro_del.html"
    success_url = reverse_lazy('catastro:catastro_list')


@login_required(login_url='login')
@permission_required('catastro.change_catastro', login_url='sin_privilegio')
def catastro_inactivar(request, id):

    catastro = Catastro.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/catastro_inactivar.html'

    if not catastro:

        return redirect('catastro:catastro_list')

    if request.method == 'GET':

        contexto = {'object': catastro}

    if request.method == 'POST':

        catastro.estado = False
        catastro.save()
        return redirect('catastro:catastro_list')

    return render(request, template_name, contexto)


@login_required(login_url='login')
@permission_required('catastro.change_catastro', login_url='sin_privilegio')
def catastro_suspender_servicio(request, id):

    catastro = Catastro.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/catastro_suspender.html'

    if not catastro:

        return redirect('catastro:catastro_list')

    if request.method=='GET':

        contexto = {'object':catastro}

    if request.method == 'POST':

        catastro.suspender = True
        catastro.save()
        return redirect('catastro:catastro_list')
    
    return render(request, template_name, contexto)


#CRUD TipoLectura =======================================================

class TipoLecturaList(SinPrivilegios, ListView):

    permission_required = 'catastro.view_tipolectura'
    model = TipoLectura


class TipoLecturaCreate(VistaBaseCreate):
    
    permission_required = 'catastro.add_tipolectura'
    model = TipoLectura
    template_name = "catastro/tipolectura_form.html"
    form_class = TipoLecturaForm
    success_url = reverse_lazy('catastro:tipolectura_list')


class TipoLecturaUpdate(VistaBaseUpdate):
    
    permission_required = 'catastro.change_tipolectura'
    model = TipoLectura
    template_name = "catastro/tipolectura_form.html"
    form_class = TipoLecturaForm
    success_url = reverse_lazy('catastro:tipolectura_list')


class TipoLecturaDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_tipolectura'
    model = TipoLectura
    template_name = "catastro/tipolectura_del.html"
    success_url = reverse_lazy('catastro:tipolectura_list')


@login_required(login_url='login')
@permission_required('catastro.change_tipolectura', login_url='sin_privilegio')
def tipolectura_inactivar(request,id):

    tipo_lectura = TipoLectura.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/tipolectura_inactivar.html'

    if not tipo_lectura:

        return redirect('catastro:tipolectura_list')
    
    if request.method=='GET':

        contexto = {'object':tipo_lectura}
    
    if request.method=='POST':

        tipo_lectura.estado = False
        tipo_lectura.save()
        return redirect('catastro:tipolectura_list')
    
    return render(request,template_name,contexto)

#CRUD Lectura =======================================================


class LecturaList(SinPrivilegios, ListView):
    
    permission_required = 'catastro.view_lectura'
    model = Lectura


class LecturaDelete(SinPrivilegios, DeleteView):

    permission_required = 'catastro.delete_lectura'
    model = Lectura
    template_name = "catastro_del.html"

@login_required(login_url='login')
@permission_required('catastro.change_lectura', login_url='sin_privilegio')
def lectura_inactivar(request, id):

    lectura = Lectura.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'catastro/lectura_inactivar.html'

    if not lectura:
        redirect('catastro:lectura_list')
    
    if request.method=='GET':
        contexto = {'object':lectura}

    if request.method=='POST':
        lectura.estado = False
        lectura.save()
        redirect('catastro:lectura_list')
    
    return render(request, template_name, contexto)


@login_required(login_url='login')
@permission_required('catastro.view_lectura', login_url='sin_privilegio')
def lectura(request, lectura_id=None):
    
    template_name='catastro/lectura_create.html'
    cat = Catastro.objects.filter(estado=True, suspender = False)
    tipo_lectura = TipoLectura.objects.filter(estado=True)
    form_lectura={}
    contexto ={}
    tarifa = 0
    valor_excedente = 0
    valor_consumo_maximo = 0
    excedente = 0
    rango_inicial = 0

    if request.method=='GET':

        form_lectura = LecturaForm()
        #Filtramos la información que visualizamos en pantalla
        enc = Lectura.objects.filter(pk=lectura_id).first()
        
        if enc:
            
            det = LecturaDetalle.objects.filter(lectura=enc)
            periodo = datetime.date.isoformat(enc.periodo)
            e = {
                'periodo':periodo,
                'descripcion':enc.descripcion,
                'consumo_total': enc.consumo_total,
                'total_base':enc.total_base,
                'total_base_reserva': enc.total_base_reserva,
                'total_excedente': enc.total_excedente,
                'total_consumo_maximo': enc.total_consumo_maximo,
                'total_general': enc.total_general,
            }
            #Rendirizamos el formulario con los campos que devuelve enc.
            form_lectura = LecturaForm(e)
            
        else:
            det =None
        
        contexto={'catastro':cat,'encabezado':enc,'detalle':det,'form_enc':form_lectura,'tipo_lectura':tipo_lectura}
    
    if request.method=='POST':
        periodo = request.POST.get('periodo')
        descripcion = request.POST.get('descripcion')
        consumo_total = 0
        total_base = 0
        total_base_reserva=0
        total_excedente = 0
        total_consumo_maximo = 0
        total_general = 0

        #si no se envia lectura_id quiere decir que el encabezado no existe
        if not lectura_id:
            #prov = Proveedor.objects.get(pk=proveedor)
            enc = Lectura(
                periodo=periodo,
                descripcion = descripcion,
                uc = request.user
            )
            if enc:
                enc.save() #grava encabezado nuevo
                lectura_id = enc.id
        else: # Editar encabezado
            enc=Lectura.objects.filter(pk=lectura_id).first()
            if enc:
                enc.periodo = periodo
                enc.descripcion = descripcion
                enc.um = request.user.id
                enc.save()

        if not lectura_id:
            return redirect('catastro:lectura_list')
        
        catastro =request.POST.get("catastro")
        lectura_anterior = request.POST.get("lectura_anterior")
        lectura_actual = request.POST.get("lectura_actual")
        consumo = request.POST.get("consumo")
        tl = request.POST.get('tipo_lectura')
        tipo = TipoLectura.objects.filter(pk=tl).first()
        tarifas = Tarifa.objects.filter(estado=True)
        catas = Catastro.objects.filter(pk=catastro).first()
        base = catas.servicio.base
        base_reserva=catas.servicio.base_reserva

        if int(consumo) > catas.servicio.base_consumo:
            
            for tar in tarifas:
                if int(consumo) >= tar.rango_inicial and int(consumo) <= tar.rango_superior:
                    tarifa = tar
                    excedente = tar.valor_excedente
                    rango_inicial = tar.rango_inicial
                    valor_consumo_maximo = 0
                    metros_excedidos = int(consumo) - rango_inicial
                    valor_excedente = metros_excedidos * excedente
                     
                elif int(consumo) > catas.servicio.consumo_maximo:
                    maximo = Tarifa.objects.aggregate(Max('rango_superior'))
                    tarif = Tarifa.objects.filter(rango_superior=maximo['rango_superior__max']).first()
                    tarifa = tarif
                    excedente = tarif.valor_excedente
                    rango_inicial = tarif.rango_inicial
                    valor_consumo_maximo = catas.servicio.valor_consumo_maximo
                    metros_excedidos = int(consumo) - rango_inicial
                    valor_excedente = metros_excedidos * excedente

        else:
            for tar in tarifas:
                if int(consumo) >= tar.rango_inicial and int(consumo) <= tar.rango_superior:
                    tarifa = tar
            valor_excedente = 0
            valor_consumo_maximo = 0

        det = LecturaDetalle(
            lectura = enc,
            catastro = catas,
            lectura_anterior = lectura_anterior,
            lectura_actual = lectura_actual,
            tarifa = tarifa,
            valor_excedente = valor_excedente,
            base = base,
            base_reserva=base_reserva,
            valor_consumo_maximo=valor_consumo_maximo,
            tipo_lectura=tipo,
            uc = request.user

        )
        if det:
            det.save()

            consumo_total = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('consumo'))
            total_base = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('base'))
            total_base_reserva = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('base_reserva'))
            total_excedente = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('valor_excedente'))
            total_consumo_maximo = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('valor_consumo_maximo'))
            total_general = LecturaDetalle.objects.filter(
                lectura=lectura_id).aggregate(Sum('total'))

            enc.consumo_total = consumo_total['consumo__sum']
            enc.total_base = total_base['base__sum']
            enc.total_base_reserva = total_base_reserva['base_reserva__sum']
            enc.total_excedente = total_excedente['valor_excedente__sum']
            enc.total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
            enc.total_general = total_general['total__sum']
            enc.save()
        
        return redirect('catastro:lectura_update', lectura_id=lectura_id)

    return render(request, template_name, contexto)


""" class LectruaDetalleUpdate(VistaBaseUpdate):
    
    permission_required = 'catastro.change_lecturadetalle'
    model = LecturaDetalle
    template_name = "catastro/lecturadetalle_form.html"
    form_class = LectruaDetalleForm

    def get_success_url(self):
        lectura_id = self.kwargs['lectura_id']
        return reverse_lazy('catastro:lectura_update', kwargs={'lectura_id': lectura_id})

 """
class LecturaDetalleDelete(SinPrivilegios, DeleteView):
    
    permission_required = 'catastro.delete_lecturadetalle'
    model = LecturaDetalle
    template_name = "catastro/lecturadetalle_del.html"

    def get_success_url(self):
        lectura_id = self.kwargs['lectura_id']
        return reverse_lazy('catastro:lectura_update', kwargs={'lectura_id': lectura_id})

def search(request):
    today = timezone.now()
    query = request.GET.get('q','')
    template_name = 'catastro/abonado_search.html'
    if query:
        qset=(
            Q(apellidos__icontains=query)|
            Q(nombres__icontains=query)
        )
        results = Abonado.objects.filter(qset).distinct()
    else:
        results=[]
    
    return render(request, template_name, {'results':results, 'query':query, 'today':today})
    

