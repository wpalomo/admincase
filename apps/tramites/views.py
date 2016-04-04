
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TramiteForm

from apps.clientes.models import Cliente
from apps.complementos.organigrama.models import Entidad
from apps.personas.models import Persona
from apps.tramites.models import (Tramite, RequisitoRequerido, TipoTramite,
                                  Requisito)


# def home(request):
#     if request.user.is_authenticated():
#         return render(request, 'tramites/home.html')


class TramiteListView(ListView):
    model = Tramite
    paginate_by = 10

    def get(self, request, *args, **kwargs):

        tramites_entidades = Entidad.objects.all()

        return render_to_response(
            'tramites/tramite_list.html',
            {
                'tramites_entidades_list': tramites_entidades
            },
            context_instance=RequestContext(request)
        )


class TramiteCreate(CreateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):
        form = TramiteForm()
        persona = Persona.objects.get(pk=kwargs['pk'])

        print(persona)

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'persona': persona
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        print(self.request.POST)

        form = TramiteForm(data=self.request.POST)

        persona = Persona.objects.get(pk=self.request.POST['persona'])

        if form.is_valid():

            tramite = form.save()

            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')

            return HttpResponseRedirect('/tramites/modi/' + str(tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'persona': persona
                # 'tipos_tramites': tipos_tramites
            },
            context_instance=RequestContext(request)
        )


class TramiteUpdate(UpdateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):

        print(kwargs['pk'])

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        # tipo_tramite = TipoTramite.objects.get(pk=tramite.tipo.id)
        #
        # requisitos = tipo_tramite.requisitos.all()

        form = TramiteForm(instance=tramite)

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'tramite': tramite
                # 'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        requisitos = RequisitoRequerido.objects.filter(tramite=tramite)

        form = TramiteForm(self.request.POST, instance=tramite)

        tipos_tramites = TipoTramite.objects.filter(
            entidad__nombre=tramite.tipo.entidad.nombre.upper())

        if form.is_valid():
            form.save()

            requisitos_presentados = self.request.POST[
                'requisitos_presentados'].split('|')

            for item in requisitos_presentados:

                requisito = item.split('#')

                if int(requisito[1]) != 0:
                    requisito_requerido = requisitos.get(
                        requisito__descripcion=requisito[0])
                    requisito_requerido.presentado = True

                else:
                    requisito_requerido = requisitos.get(
                        requisito__descripcion=requisito[0])
                    requisito_requerido.presentado = False

                requisito_requerido.save()

            messages.add_message(
                request, messages.SUCCESS, 'SE HA ACTUALIZADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'tramite': tramite,
                'requisitos': requisitos,
                'tipos_tramites': tipos_tramites
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class TramiteClienteListView(ListView):
    model = Tramite
    paginate_by = 10

    def get(self, request, *args, **kwargs):

        tramite_cliente = Tramite.objects.filter(persona__id=kwargs['pk'])
        cliente = Cliente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'tramites/tramite_cliente_list.html',
            {
                'cliente': cliente,
                'tramite_cliente': tramite_cliente
            },
            context_instance=RequestContext(request)
        )


# ANSES #

class AnsesTramitesListView(ListView):
    queryset = TipoTramite.objects.filter(
        entidad__nombre='ANSES'
    )
    context_object_name = 'cliente_anses'
    template_name = 'tramites/tramite_anses_list.html'
    paginate_by = 10


# CAJA - PREVISION #

class CajaPrevisionListView(ListView):
    queryset = Tramite.objects.filter(
        tipo__entidad__nombre='CAJA',
        estado=False
    )
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


class CajaPrevisionTramitesListView(ListView):
    queryset = Tramite.objects.filter(
        tipo__entidad__nombre='CAJA',
        estado=False
    )
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


# FAMILIA #

class FamiliaListView(ListView):
    model = Cliente
    template_name = 'tramites/tramite_familia_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(FamiliaListView, self).get_context_data(*args, **kwargs)
        # context['tipo_tramite_familia'] = Tramite.objects.filter(entidad__id=3)
        return context


class FamiliaTramitesListView(ListView):
    model = Cliente
    template_name = 'tramites/tramite_familia_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(FamiliaListView, self).get_context_data(*args, **kwargs)
        # context['tipo_tramite_familia'] = Tramite.objects.filter(entidad__id=3)
        return context


class CivilComercialListView(ListView):
    model = Cliente
    # queryset = Tramite.objects.filter(entidad__id=4)
    context_object_name = 'cliente_civil_comercial'
    template_name = 'tramites/tramite_civilcomercial_list.html'
    paginate_by = 10

