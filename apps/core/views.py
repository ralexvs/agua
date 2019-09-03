from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from apps.recaudacion.models import Recaudacion, RecaudacionDetalle
from django.db.models import Sum
import datetime
from django.utils import timezone


# Create your views here.

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
    
    recaudado = Recaudacion.objects.filter(estado=True)
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

        
        contexto = {'recaudado': recaudado, 
                    'alcantarillado': total_alcantarillado, 
                    'administracion':total_administracion,
                    'agua': agua,
                    'descuentos':descuentos,
                    'subtotal': subtotal,
                    'total_recaudado': total_recaudado,
                    'ahora':timezone.now(),

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

    success_message = "Su registro, ha sido actualizado"

    def form_valid(self, form):

        form.instance.um = self.request.user.id
        return super().form_valid(form)


class VistaBaseDelete(SuccessMessageMixin, SinPrivilegios, DeleteView):

    success_message = "Su registro, fue eliminado"
