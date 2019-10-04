from django.shortcuts import render, redirect
from .models import Entidad, Servicio, Tarifa, Multa, Descuento, Pago
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from apps.core.views import SinPrivilegios, VistaBaseCreate, VistaBaseUpdate, VistaBaseDelete
from django.urls import reverse_lazy
from .forms import EntidadForm, ServicioForm, TarifaForm, MultaForm, DescuentoForm, PagoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

# Create your views here.

#CRUD Entidad =======================================================
class EntidadList(SinPrivilegios, ListView):
    
    permission_required = 'parametro.view_entidad'
    model = Entidad
    #template_name = ".html"
    #context_object_name = 'obj'


class EntidadCreate(VistaBaseCreate):

    permission_required = 'parametro.add_entidad'
    model = Entidad
    template_name = "parametro/entidad_form.html"
    form_class = EntidadForm
    success_url = reverse_lazy('parametro:entidad_list')


class EntidadUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_entidad'
    model = Entidad
    template_name = "parametro/entidad_form.html"
    form_class = EntidadForm
    success_url = reverse_lazy('parametro:entidad_list')


class EntidadDelete(VistaBaseDelete):

    permission_required = 'parametro.delete_entidad'
    model = Entidad
    template_name = "parametro/entidad_del.html"
    success_url = reverse_lazy('parametro:entidad_list')


@login_required(login_url='login')
@permission_required('parametro.change_entidad', login_url='sin_privilegio')
def entidad_inactivar(request, id):
    entidad = Entidad.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/entidad_inactivar.html'

    if not entidad:
        return redirect('parametro:entidad_list')

    if request.method == 'GET':
        contexto = {'object': entidad}

    if request.method == 'POST':
       
        entidad.estado = False
        entidad.save()
        messages.success(request, 'Ha sido inactivada su entidad')

        return redirect('parametro:entidad_list')

    return render(request, template_name, contexto)



 #CRUD Servicio =======================================================

class ServicioList(SinPrivilegios, ListView):

    permission_required = 'parametro.view_servicio'
    model = Servicio
    #template_name = ".html"
    #context_object_name = 'obj'


class ServicioCreate(VistaBaseCreate):

    permission_required = 'parametro.add_servicio'
    model = Servicio
    template_name = "parametro/servicio_form.html"
    form_class = ServicioForm
    success_url = reverse_lazy('parametro:servicio_list')

   
class ServicioUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_servicio'
    model = Servicio
    template_name = "parametro/servicio_form.html"
    form_class = ServicioForm
    success_url = reverse_lazy('parametro:servicio_list')


class ServicioDelete(VistaBaseDelete):

    permission_required = 'parametro.delete_servicio'
    model = Servicio
    template_name = "parametro/servicio_del.html"
    success_url = reverse_lazy('parametro:servicio_list')


@login_required(login_url='login')
@permission_required('parametro.change_servicio', login_url='sin_privilegio')
def servicio_inactivar(request, id):

    servicio = Servicio.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/servicio_inactivar.html'

    if not servicio:

        return redirect('parametro:servicio_list')

    if request.method == 'GET':

        contexto = {'object': servicio}

    if request.method == 'POST':

        servicio.estado = False
        servicio.save()
        return redirect('parametro:servicio_list')

    return render(request, template_name, contexto)


#CRUD Tarifa =======================================================

class TarifaList(SinPrivilegios, ListView):

    permission_required = 'parametro.view_tarifa'
    model = Tarifa
    #template_name = ".html"
    #context_object_name = 'obj'


class TarifaCreate(VistaBaseCreate):

    permission_required = 'parametro.add_tarifa'
    model = Tarifa
    template_name = "parametro/tarifa_form.html"
    form_class = TarifaForm
    success_url = reverse_lazy('parametro:tarifa_list')

class TarifaUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_tarifa'
    model = Tarifa
    template_name = "parametro/tarifa_form.html"
    form_class = TarifaForm
    success_url = reverse_lazy('parametro:tarifa_list')


class TarifaDelete(VistaBaseDelete):

    permission_required = 'parametro.delete_tarifa'
    model = Tarifa
    template_name = "parametro/tarifa_del.html"
    success_url = reverse_lazy('parametro:tarifa_list')


@login_required(login_url='login')
@permission_required('parametro.change_tarifa', login_url='sin_privilegio')
def tarifa_inactivar(request, id):

    tarifa = Tarifa.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/tarifa_inactivar.html'

    if not tarifa:

        return redirect('parametro:tarifa_list')

    if request.method == 'GET':

        contexto = {'object': tarifa}

    if request.method == 'POST':

        tarifa.estado = False
        tarifa.save()
        return redirect('parametro:tarifa_list')

    return render(request, template_name, contexto)


#CRUD Multa =======================================================

class MultaList(SinPrivilegios, ListView):

    permission_required = 'parametro.view_multa'
    model = Multa


class MultaCreate(VistaBaseCreate):

    permission_required = 'parametro.add_multa'
    model = Multa
    template_name = "parametro/multa_form.html"
    form_class = MultaForm
    success_url = reverse_lazy('parametro:multa_list')

 
class MultaUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_multa'
    model = Multa
    template_name = "parametro/multa_form.html"
    form_class = MultaForm
    success_url = reverse_lazy('parametro:multa_list')

   
class MultaDelete(VistaBaseDelete):

    permission_required = 'parametro.delete_multa'
    model = Multa
    template_name = "parametro/multa_del.html"
    success_url = reverse_lazy('parametro:multa_list')


@login_required(login_url='login')
@permission_required('parametro.change_multa', login_url='sin_privilegio')
def multa_inactivar(request, id):

    multa = Multa.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/multa_inactivar.html'

    if not multa:

        return redirect('parametro:multa_list')

    if request.method == 'GET':

        contexto = {'object': multa}

    if request.method == 'POST':

        multa.estado = False
        multa.save()
        return redirect('parametro:multa_list')

    return render(request, template_name, contexto)


#CRUD Descuento =======================================================

class DescuentoList(SinPrivilegios, ListView):

    permission_required = 'parametro.view_descuento'
    model = Descuento


class DescuentoCreate(VistaBaseCreate):

    permission_required = 'parametro.add_descuento'
    model = Descuento
    template_name = "parametro/descuento_form.html"
    form_class = DescuentoForm
    success_url = reverse_lazy('parametro:descuento_list')


class DescuentoUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_descuento'
    model = Descuento
    template_name = "parametro/descuento_form.html"
    form_class = DescuentoForm
    success_url = reverse_lazy('parametro:descuento_list')

   

class DescuentoDelete(VistaBaseDelete):

    permission_required = 'parametro.delete_descuento'
    model = Descuento
    template_name = "parametro/descuento_del.html"
    success_url = reverse_lazy('parametro:descuento_list')


@login_required(login_url='login')
@permission_required('parametro.change_descuento', login_url='sin_privilegio')
def descuento_inactivar(request, id):

    descuento = Descuento.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/descuento_inactivar.html'

    if not descuento:

        return redirect('parametro:descuento_list')

    if request.method == 'GET':

        contexto = {'object': descuento}

    if request.method == 'POST':

        descuento.estado = False
        descuento.save()
        return redirect('parametro:descuento_list')

    return render(request, template_name, contexto)


#CRUD Pago =======================================================

class PagoList(SinPrivilegios, ListView):

    permission_required = 'parametro.view_pago'
    model = Pago


class PagoCreate(VistaBaseCreate):

    permission_required = 'parametro.add_pago'
    model = Pago
    template_name = "parametro/pago_form.html"
    form_class = PagoForm
    success_url = reverse_lazy('parametro:pago_list')


class PagoUpdate(VistaBaseUpdate):

    permission_required = 'parametro.change_pago'
    model = Pago
    template_name = "parametro/pago_form.html"
    form_class = PagoForm
    success_url = reverse_lazy('parametro:pago_list')


class PagoDelete(SinPrivilegios, DeleteView):

    permission_required = 'parametro.delete_pago'
    model = Pago
    template_name = "parametro/pago_del.html"
    success_url = reverse_lazy('parametro:pago_list')


@login_required(login_url='login')
@permission_required('parametro.change_pago', login_url='sin_privilegio')
def pago_inactivar(request, id):

    pago = Pago.objects.filter(pk=id).first()
    contexto = {}
    template_name = 'parametro/pago_inactivar.html'

    if not pago:

        return redirect('parametro:pago_list')

    if request.method == 'GET':

        contexto = {'object': pago}

    if request.method == 'POST':

        pago.estado = False
        pago.save()
        return redirect('parametro:pago_list')

    return render(request, template_name, contexto)
