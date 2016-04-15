# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from .forms import PerfilForm, PerfilModuloForm
from .models import Perfil, PerfilModulo


class PerfilCreate(CreateView):

    model = Perfil
    form_class = PerfilForm

    def post(self, request, *args, **kwargs):

        form = PerfilForm(data=self.request.POST)

        if form.is_valid():

            form.save()

            messages.add_message(
                request, messages.SUCCESS, 'PERFIL CREADO CON EXITO')

            return HttpResponseRedirect('/seguridad/perfil/alta/')

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'seguridad/perfil_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


class PerfilUpdate(UpdateView):

    model = Perfil
    form_class = PerfilForm

    def post(self, request, *args, **kwargs):

        perfil = Perfil.objects.get(pk=kwargs['pk'])
        form = PerfilForm(data=self.request.POST, instance=perfil)

        if form.is_valid():

            perfil = form.save()

            messages.add_message(
                request, messages.SUCCESS, 'PERFIL MODIFICADO CON EXITO')

            return HttpResponseRedirect(
                '/seguridad/perfil/modi/' + str(perfil.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'seguridad/perfil_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


class PerfilDelete(DeleteView):

    """
    AUTOMATICAMENTE SE ELIMINAN LOS REGISTROS RELACIONADOS ENTRE MODELOS.
    PerfilModulo
    """

    model = Perfil
    template_name = 'seguridad/perfil_delete.html'

    def get_success_url(self):
        return '/seguridad/perfil/listado'


class PerfilListView(ListView):

    model = Perfil
    paginate_by = 200

    def get_queryset(self):

        if self.request.GET.get('filtro') == 'TODOS':

            query = Perfil.objects.all()

        elif self.request.GET.get('filtro') == 'NOMBRE':

            nombre = self.request.GET.get('nombre')
            query = self.buscar_por_nombre(nombre)

        else:

            query = super(PerfilListView, self).get_queryset()

        return query

    def buscar_por_nombre(self, nombre):

        try:
            perfiles = Perfil.objects.filter(nombre__icontains=nombre)
        except:
            perfiles = None

        return perfiles


#-------------------------------------------------------------
#-------------- PERFIL - MODULOS -----------------------------
#-------------------------------------------------------------


class PerfilModuloCreate(CreateView):

    model = PerfilModulo
    form_class = PerfilModuloForm

    def get(self, request, *args, **kwargs):

        perfil = Perfil.objects.get(pk=kwargs['pk'])
        modulo_perfil = PerfilModulo.objects.filter(perfil=perfil)
        form = PerfilModuloForm()

        return render_to_response(
            'seguridad/perfilmodulo_form.html',
            {'form': form, 'perfil': perfil, 'modulo_perfil': modulo_perfil},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = PerfilModuloForm(data=self.request.POST)

        if form.is_valid():

            perfil_modulo = form.save()

            messages.add_message(
                request, messages.SUCCESS, 'MODULO AGREGADO AL PERFIL')

            return HttpResponseRedirect(
                '/seguridad/perfil/modulos/' + str(perfil_modulo.perfil_id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'seguridad/perfilmodulo_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


class PerfilModuloDelete(DeleteView):

    model = PerfilModulo
    template_name = 'seguridad/perfilmodulo_delete.html'

    def dispatch(self, *args, **kwargs):
        perfil_modulo = PerfilModulo.objects.get(id=kwargs['pk'])
        self.perfil_id = perfil_modulo.perfil.id
        return super(PerfilModuloDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/seguridad/perfil/modulos/' + str(self.perfil_id)