from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from apps.recaudacion.models import Recaudacion, RecaudacionDetalle
from apps.catastro.models import Lectura, LecturaDetalle
from apps.parametro.models import Entidad
from django.db.models import Sum
from django.http import JsonResponse
import json as simplejson
from random import randint
import datetime
from datetime import time, date
from django.utils import timezone

# Create your views here.

def get_coords(request, *args, **kwargs):
    template_name = 'core/charts.html'
    datos = Lectura.objects.all()
    voto = []
    texto = []
    color = []
    i = 0
    for item in datos:
        texto.append(item.descripcion)
        r = lambda: randint(0,255)
        r = lambda: randint(0, 255)
        color.append('#%02X%02X%02X' % (r(),r(),r()))
        voto.append(item.consumo_total)
        i +=1
    pregunta = simplejson.dumps(texto)
    voto = simplejson.dumps(voto)
    color = simplejson.dumps(color)
    context={
        'pregunta':pregunta,
        'voto': voto,
        'color':color,
        'datos':datos,
        'i':i
    }
    return render(request, template_name, context)

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'login'
    raise_exception = False
    redirect_field_name = 'redirect_to'

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser

        if not self.request.user == AnonymousUser():
            self.login_url = 'sin_privilegio'
        return HttpResponseRedirect(reverse_lazy(self.login_url))



def home(request):
    contexto = {}
    template_name = "core/home.html"
    entidad = Entidad.objects.all().first()
    recaudado = Recaudacion.objects.filter(estado=True)
    deudores = LecturaDetalle.objects.filter(estado=True)

    datos = Lectura.objects.all()
    voto = []
    texto = []
    color = []
    i = 0
    for item in datos:
        texto.append(item.descripcion)
        r = lambda: randint(0, 255)
        r = lambda: randint(0, 255)
        color.append('#%02X%02X%02X' % (r(), r(), r()))
        voto.append(item.consumo_total)
        i += 1
    pregunta = simplejson.dumps(texto)
    voto = simplejson.dumps(voto)
    color = simplejson.dumps(color)




    if recaudado:
        total_base = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('base'))
        total_base_reserva = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('base_reserva'))
        total_excedente = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('valor_excedente'))
        total_consumo_maximo = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('valor_consumo_maximo'))
        total_administracion = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('administracion'))
        total_alcantarillado = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('alcantarillado'))
        total_derecho_conexion = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('derecho_conexion'))
        total_general = RecaudacionDetalle.objects.filter(
            estado=True).aggregate(Sum('total'))

        total_base = total_base['base__sum']
        total_base_reserva = total_base_reserva['base_reserva__sum']
        total_excedente = total_excedente['valor_excedente__sum']
        total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
        total_administracion = total_administracion['administracion__sum']
        total_alcantarillado = total_alcantarillado['alcantarillado__sum']
        total_derecho_conexion = total_derecho_conexion['derecho_conexion__sum']
        
        agua = total_base + total_base_reserva+total_excedente + total_consumo_maximo + total_derecho_conexion
        
        descuentos = Recaudacion.objects.all().aggregate(Sum('total_descuento'))
        
        subtotal = Recaudacion.objects.all().aggregate(Sum('subtotal'))
        total_recaudado = Recaudacion.objects.all().aggregate(Sum('total_general'))

        descuentos = descuentos['total_descuento__sum']

        if deudores:
            total = LecturaDetalle.objects.filter(estado = True).aggregate(Sum('total'))
        else:
            total = 0
    
        contexto = {'recaudado': recaudado, 
                    'alcantarillado': total_alcantarillado, 
                    'administracion':total_administracion,
                    'agua': agua,
                    'descuentos':descuentos,
                    'subtotal': subtotal,
                    'total_recaudado': total_recaudado,
                    'ahora':timezone.now(),
                    'deudores':deudores,
                    'total':total,
                    'pregunta': pregunta,
                    'voto': voto,
                    'color': color,
                    'datos': datos,
                    'i': i,
                    'entidad':entidad,
        }
    #queryset = RecaudacionDetalle.objects.filter(estado=True)
    return render(request, template_name,contexto)

class HomeSinPrivilegios(LoginRequiredMixin, TemplateView):
    template_name = "core/sin_privilegio.html"
    login_url = 'login'

#VISTAS BASES


class VistaBaseCreate(SuccessMessageMixin, SinPrivilegios, CreateView):

    success_message = "Registro, agregado satisfactoriamente"
    def form_valid(self, form):

        form.instance.uc = self.request.user
        return super().form_valid(form)


class VistaBaseUpdate(SuccessMessageMixin, SinPrivilegios, UpdateView ):

    success_message = "Registro, ha sido actualizado"

    def form_valid(self, form):

        form.instance.um = self.request.user.id
        return super().form_valid(form)


class VistaBaseDelete(SuccessMessageMixin, SinPrivilegios, DeleteView):

    success_message = "Registro, fue eliminado"
