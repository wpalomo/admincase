
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TramiteForm

from apps.clientes.models import Cliente
from apps.complementos.organigrama.models import Entidad
from apps.personas.models import Persona
from apps.tramites.models import (Tramite, RequisitoTramite, TipoTramite,
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

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = TramiteForm(data=self.request.POST)

        cliente = Cliente.objects.get(pk=int(self.request.POST['cliente']))

        if form.is_valid():
            tramite = form.save()

            requisitos_tramite = self.request.POST['requisitos_presentados']

            if requisitos_tramite:
                parametros = requisitos_tramite.split("|")

                for item in parametros:
                    print(item)
                    requisito_parametro = item.split("#")

                    requisito = Requisito.objects.get(
                        valor=requisito_parametro[0])
                    # presentado = 0
                    # if requisito_parametro[1] == 1:
                    #     presentado = 1
                    print(requisito_parametro[1])
                    presentado = (False, True)[requisito_parametro[1] == '1']

                    RequisitoTramite.objects.create(
                        tramite=tramite,
                        requisito=requisito,
                        presentado=presentado
                    )

            messages.add_message(
                request, messages.SUCCESS, 'EL TRAMITE SE HA CREADO CON EXITO')

            return HttpResponseRedirect('/tramites/modi/' + str(tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente
                # 'tipos_tramites': tipos_tramites
            },
            context_instance=RequestContext(request)
        )


class TramiteUpdate(UpdateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):


        tramite = Tramite.objects.get(pk=kwargs['pk'])
        cliente = Cliente.objects.get(pk=tramite.cliente.id)
        requisitos_tramite = tramite.requisitotramite_set.all()

        form = TramiteForm(instance=tramite)

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente,
                'requisitos': requisitos_tramite
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        requisitos_tramite = tramite.requisitotramite_set.all()

        form = TramiteForm(self.request.POST, instance=tramite)

        if form.is_valid():
            form.save()

            requisitos = self.request.POST['requisitos_presentados']

            if requisitos:
                parametros = requisitos.split("|")

                print(requisitos)

                for item in parametros:
                    requisito_parametro = item.split("#")
                    requisito = RequisitoTramite.objects.get(
                        requisito__valor=requisito_parametro[0])
                    presentado = (False, True)[requisito_parametro[1] == '1']
                    requisito.presentado = presentado
                    requisito.save()

            messages.add_message(
                request, messages.SUCCESS,
                'EL TRAMITE SE HA ACTUALIZADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'tramite': tramite,
                'requisitos': requisitos_tramite
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class TramiteClienteListView(ListView):
    model = Tramite
    paginate_by = 10

    def get(self, request, *args, **kwargs):

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        tramite_cliente = Tramite.objects.filter(cliente__id=cliente.id)

        return render_to_response(
            'tramites/tramite_cliente_list.html',
            {
                'cliente': cliente,
                'tramite_cliente': tramite_cliente
            },
            context_instance=RequestContext(request)
        )


# ANSES #
#
# class AnsesTramitesListView(ListView):
#     queryset = TipoTramite.objects.filter(
#         entidad__nombre='ANSES'
#     )
#     context_object_name = 'cliente_anses'
#     template_name = 'tramites/tramite_anses_list.html'
#     paginate_by = 10
#

# CAJA - PREVISION #
#
# class CajaPrevisionListView(ListView):
#     queryset = Tramite.objects.filter(
#         tipo__entidad__nombre='CAJA',
#         estado=False
#     )
#     context_object_name = 'cliente_caja'
#     template_name = 'tramites/tramite_caja_list.html'
#     paginate_by = 10
#
#
# class CajaPrevisionTramitesListView(ListView):
#     queryset = Tramite.objects.filter(
#         tipo__entidad__nombre='CAJA',
#         estado=False
#     )
#     context_object_name = 'cliente_caja'
#     template_name = 'tramites/tramite_caja_list.html'
#     paginate_by = 10

#
# # FAMILIA #
#
# class FamiliaListView(ListView):
#     model = Cliente
#     template_name = 'tramites/tramite_familia_list.html'
#     paginate_by = 10
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(FamiliaListView, self).get_context_data(*args, **kwargs)
#         # context['tipo_tramite_familia'] = Tramite.objects.filter(entidad__id=3)
#         return context
#
#
# class FamiliaTramitesListView(ListView):
#     model = Cliente
#     template_name = 'tramites/tramite_familia_list.html'
#     paginate_by = 10
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(FamiliaListView, self).get_context_data(*args, **kwargs)
#         # context['tipo_tramite_familia'] = Tramite.objects.filter(entidad__id=3)
#         return context
#
#
# class CivilComercialListView(ListView):
#     model = Cliente
#     # queryset = Tramite.objects.filter(entidad__id=4)
#     context_object_name = 'cliente_civil_comercial'
#     template_name = 'tramites/tramite_civilcomercial_list.html'
#     paginate_by = 10

