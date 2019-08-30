from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from apps.catastro.models import Lectura, LecturaDetalle, Abonado
from apps.recaudacion.models import Recaudacion
from django.db.models import Sum


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



class Home(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    login_url = 'login'





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


def dashboard(request):
    contexto={}
    
    #Totales 
    total_emitido = Lectura.objects.all().aggregate(Sum('total_general'))
    total_pendiente = LecturaDetalle.objects.filter(estado = True).aggregate(Sum('total'))
    total_recaudado = Recaudacion.objects.all().aggregate(Sum('total_general'))
    total_descuento = Recaudacion.objects.all().aggregate(Sum('total_descuento'))

    emitido = total_emitido['total_general__sum']
    pendiente = total_pendiente['total__sum']
    recaudado = total_recaudado['total_general__sum']
    descuento = total_descuento['total_descuento__sum']
    template_name = "core/home.html"
    
    #Ultimos 5 abonados
    abonado = Abonado.objects.filter().order_by('-id')[0:3]

    
    contexto = {'emitido': emitido,'pendiente':pendiente,'recaudado': recaudado,'descuento':descuento,'abonado':abonado}
    return render(request, template_name, contexto)
