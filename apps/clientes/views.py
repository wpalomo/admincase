
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  TemplateView)

from apps.complementos.locacion.models import (Pais, Provincia, Departamento,
                                               Localidad)
from apps.personas.models import Persona
from apps.tramites.models import Tramite

from .forms import PersonaForm, ClienteForm
from .models import Cliente


class ClienteListView(ListView):
    model = Cliente
    paginate_by = 10


class ClienteCreate(CreateView):
    model = Cliente
    form_class = PersonaForm

    def get_context_data(self, **kwargs):
        context = super(ClienteCreate, self).get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm()
        context['paises'] = Pais.objects.all()
        context['provincias'] = Provincia.objects.all()
        context['departamentos'] = Departamento.objects.all()
        context['localidades'] = Localidad.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        persona_form = PersonaForm(data=self.request.POST)
        cliente_form = ClienteForm(data=self.request.POST)

        if persona_form.is_valid() and cliente_form.is_valid():
            persona = persona_form.save()
            cliente_form.instance.persona = persona
            cliente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'CLIENTE CREADO CON EXITO')

            return HttpResponseRedirect('/clientes/modi/%s' % str(persona.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'cliente_form': cliente_form,
                'form': persona_form
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteUpdate(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'clientes/cliente_form.html'
    # modulo = 'clientes'

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdate, self).get_context_data(**kwargs)
        cliente = Cliente.objects.get(persona=self.object)
        context['cliente_form'] = ClienteForm(instance=cliente)
        context['persona'] = self.object
        context['persona_tramites'] = Tramite.objects.filter(
            persona__id=int(self.object.id))[:3]

        context['paises'] = Pais.objects.all()
        context['provincias'] = Provincia.objects.all()
        context['departamentos'] = Departamento.objects.all()
        context['localidades'] = Localidad.objects.all()

        return context

    def post(self, request, *args, **kwargs):

        persona = Persona.objects.get(pk=kwargs['pk'])
        cliente = Cliente.objects.get(persona=persona)

        persona_form = PersonaForm(self.request.POST, instance=persona)
        cliente_form = ClienteForm(self.request.POST, instance=cliente)

        if persona_form.is_valid() and cliente_form.is_valid():
            persona = persona_form.save()
            cliente_form.instance.persona = persona
            cliente_form.save()



            messages.add_message(
                request, messages.SUCCESS, 'CLIENTE MODIFICADO CON EXITO')

            return HttpResponseRedirect('/clientes/modi/%s' % kwargs['pk'])

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'cliente_form': cliente_form,
                'form': persona_form
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteDelete(DeleteView):
    model = Cliente


class ClienteAnsesListView(ListView):
    queryset = Cliente.objects.filter(
        persona__tramite__tipo__entidad__nombre='ANSES')
    context_object_name = 'cliente_anses'
    template_name = 'tramites/tramite_anses_list.html'
    paginate_by = 10


class ClienteCajaListView(ListView):
    queryset = Cliente.objects.filter(
        persona__tramite__tipo__entidad__nombre='CAJA')
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


class DomiciliosAnidadosAjax(TemplateView):

    def post(self, request, *args, **kwargs):
        id_pk = request.POST['id']
        tipo = request.POST['tipo']

        if tipo == '1':  # Provincias del pais seleccionado
            datos_serialize = Provincia.objects.filter(pais__id=id_pk)
        if tipo == '2':  # Departamentos del prov seleccionado
            datos_serialize = Departamento.objects.filter(provincias__id=id_pk)
        if tipo == '3':  # Localidades del depto seleccionado
            datos_serialize = Localidad.objects.filter(departamentos__id=id_pk)


        data = serializers.serialize('json', datos_serialize)

        return HttpResponse(data, content_type='application/json')