from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


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
