
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  TemplateView)
from apps.personas.forms import PersonaForm
from apps.personas.models import Persona

from .forms import ClienteForm
from .models import Cliente
from . import helpers


class ClienteListView(ListView):
    model = Cliente
    paginate_by = 10

    def get_queryset(self):

        query = super(ClienteListView, self).get_queryset()

        parametro1 = self.request.GET.get('parametro1')
        parametro2 = self.request.GET.get('parametro2')

        if self.request.GET.get('filtro') == 'NUMERO_EXPEDIENTE':

            query = self.buscar_por_numero(parametro1, parametro2)

        if self.request.GET.get('filtro') == 'NUMERO_RESOLUCION_PAGO':

            query = self.buscar_por_numero_resolucion_pago(parametro1)

        return query

    def buscar_por_numero(self, numero, anio):

        numero = numero.strip()
        anio = anio.strip()

        expedientes = Cliente.objects.filter(
            numero=numero,
            anio__icontains=anio
        )

        return expedientes

    def buscar_por_numero_resolucion_pago(self, numero_resolucion_pago):

        numero_resolucion_pago = numero_resolucion_pago.strip()

        expediente_resolucion_list =\
                Cliente.objects.filter(
                    numero_resolucion_pago=numero_resolucion_pago)\
                    .values('expediente_id')
        expediente_servicio_medico_list =\
            Cliente.objects.filter(
                numero_resolucion_pago=numero_resolucion_pago)\
                .values('expediente_id')

        expediente_ids = set(
            [expediente['expediente_id']
             for expediente in expediente_resolucion_list] +
            [expediente['expediente_id']
             for expediente in expediente_servicio_medico_list]
        )

        expedientes = Cliente.objects.filter(pk__in=expediente_ids)
        return expedientes


class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm

    def get(self, request, *args, **kwargs):

        persona_form = PersonaForm()
        cliente_form = ClienteForm()

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'form': persona_form,
                'cliente_form': cliente_form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        persona_form = PersonaForm(self.request.POST, self.request.FILES)
        cliente_form = ClienteForm(data=self.request.POST)

        if persona_form.is_valid() and cliente_form.is_valid():
            persona = persona_form.save(commit=False)

            if 'foto' in self.request.FILES:
                self.set_foto(persona, (self.request.FILES['foto']))
            persona.save()
            cliente_form.instance.persona = persona
            cliente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'CLIENTE CREADO CON EXITO')

            return HttpResponseRedirect('/clientes/modi/%s' % str(persona.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'empleados/empleado_form.html',
            {
                'form': persona_form,
                'empleado_form': cliente_form
            },
            context_instance=RequestContext(request)
        )

    def set_foto(self, persona, foto):
        '''
        foto.name = helpers.cambiar_nombre_imagen(
            foto.name, int(Persona.objects.latest('id').id) + 1)
        '''
        numero_documento = self.request.POST['numero_documento']

        foto.name = helpers.cambiar_nombre_imagen(
            foto.name, int(numero_documento))

        foto = helpers.redimensionar_imagen(persona.foto, foto.name)
        # Se envia foto subida y el cambio de nombre, como parametros
        persona.foto = foto

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClienteForm

    def get(self, request, *args, **kwargs):

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        persona = Persona.objects.get(pk=cliente.persona.id)
        persona_form = PersonaForm(instance=persona)

        cliente_form = ClienteForm(instance=cliente)

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'form': persona_form,
                'cliente_form': cliente_form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(pk=kwargs['pk'])
        persona = Persona.objects.get(pk=cliente.persona.id)

        persona_form = PersonaForm(self.request.POST, self.request.FILES,
                                   instance=persona)
        cliente_form = ClienteForm(self.request.POST, instance=cliente)

        if persona_form.is_valid() and cliente_form.is_valid():

            if 'foto' in self.request.FILES:
                self.set_foto(persona_form, self.request.FILES['foto'])

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
                'form': persona_form,
                'cliente_form': cliente_form
            },
            context_instance=RequestContext(request)
        )

    def set_foto(self, persona, foto):
        foto.name = \
            helpers.cambiar_nombre_imagen(foto.name, persona.instance.id)
        persona.instance.foto = helpers.redimensionar_imagen(
            persona.instance.foto, foto.name)
        persona.save()

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteDelete(DeleteView):
    model = Cliente


# class ClienteAnsesListView(ListView):
#     queryset = Cliente.objects.filter(
#         persona__tramite__tipo__entidad__nombre='ANSES')
#     context_object_name = 'cliente_anses'
#     template_name = 'tramites/tramite_anses_list.html'
#     paginate_by = 10
#
#
# class ClienteCajaListView(ListView):
#     queryset = Cliente.objects.filter(
#         persona__tramite__tipo__entidad__nombre='CAJA')
#     context_object_name = 'cliente_caja'
#     template_name = 'tramites/tramite_caja_list.html'
#     paginate_by = 10
#
#
# class DomiciliosAnidadosAjax(TemplateView):
#
#     def post(self, request, *args, **kwargs):
#         id_pk = request.POST['id']
#         tipo = request.POST['tipo']
#
#         if tipo == '1':  # Provincias del pais seleccionado
#             datos_serialize = Provincia.objects.filter(pais__id=id_pk)
#         if tipo == '2':  # Departamentos del prov seleccionado
#             datos_serialize = Departamento.objects.filter(provincias__id=id_pk)
#         if tipo == '3':  # Localidades del depto seleccionado
#             datos_serialize = Localidad.objects.filter(departamentos__id=id_pk)
#
#
#         data = serializers.serialize('json', datos_serialize)
#
#         return HttpResponse(data, content_type='application/json')