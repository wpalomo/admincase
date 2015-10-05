
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TramiteForm

from apps.clientes.models import Cliente
from apps.personas.models import Persona
from apps.tramites.models import (Tramite, RequisitoPresentado, TipoTramite,
                                  Requisito)


# def home(request):
#     if request.user.is_authenticated():
#         return render(request, 'tramites/home.html')


class TramiteListView(ListView):
    model = Tramite
    paginate_by = 10


class TramiteCreate(CreateView):
    model = Tramite
    form_class = TramiteForm

    def post(self, request, *args, **kwargs):

        form = TramiteForm(data=self.request.POST)

        persona = Persona.objects.get(pk=self.request.POST['persona'])

        print(self.request.POST)
        print('####')
        print(persona)

        if form.is_valid():

            tramite = form.save()

            tipo_tramite = TipoTramite.objects.get(
                pk=int(self.request.POST['tipo'])
            )

            print('@@@@@@')
            print(tipo_tramite)
            print('@@@@@@')

            # ['DNI', 'ACTA DE NACIMIENTO', 'FOTO 3X3']

            for item in tipo_tramite.requisitos.all():

                print(item)

                requisito = Requisito.objects.get(descripcion=item)

                RequisitoPresentado.objects.create(
                    tramite=tramite,
                    requisito=requisito
                )


            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')


            return HttpResponseRedirect(
                '/tramites/modi/' +
                str(tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'persona': persona,
            },
            context_instance=RequestContext(request)
        )


class TramiteUpdate(UpdateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        requisitos = RequisitoPresentado.objects.filter(
            tramite=tramite)

        form = TramiteForm(instance=tramite)

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'tramite': tramite,
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        requisitos = RequisitoPresentado.objects.filter(
            tramite=tramite)

        form = TramiteForm(self.request.POST, instance=tramite)

        if form.is_valid():
            form.save()

            requisitos_presentados = self.request.POST[
                'requisitos_presentados'].split('|')

            for item in requisitos_presentados:

                print(item)

                requisito = item.split('#')

                if int(requisito[1]) != 0:

                    requisito_presentado = requisitos.get(
                        requisito__descripcion=requisito[0])
                    requisito_presentado.estado = True

                else:

                    requisito_presentado = requisitos.get(
                        requisito__descripcion=requisito[0])
                    requisito_presentado.estado = False

                requisito_presentado.save()

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
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class AnsesListView(ListView):
    queryset = Tramite.objects.filter(tipo__entidad__nombre='ANSES')
    context_object_name = 'cliente_anses'
    template_name = 'tramites/tramite_anses_list.html'
    paginate_by = 10

    # def get_context_data(self, *args, **kwargs):
    #     context = super(AnsesListView, self).get_context_data(*args, **kwargs)
    #     context['tipo_tramite_anses'] = Tramite.objects.filter(entidad__id=1)
    #     return context


class AnsesCreate(CreateView):
    model = Tramite
    form_class = TramiteForm


class AnsesUpdate(UpdateView):
    model = Tramite
    form_class = TramiteForm
    template_name = 'tramites/tramite_anses_form.html'


class CajaPrevisionListView(ListView):
    # model = Cliente
    queryset = Tramite.objects.filter(tipo__entidad__nombre='CAJA')
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


class FamiliaListView(ListView):
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

