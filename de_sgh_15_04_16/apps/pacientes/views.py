# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic import ListView, CreateView, UpdateView

from apps.personas.mixins import UrlSessionMixin
from apps.personas.models import Persona
from apps.complementos.persona.models import TipoDocumento

from .forms import PersonaForm, PacienteForm
from .models import Paciente, TipoPaciente


class PacienteCreate(CreateView):
    model = Paciente
    form_class = PersonaForm

    def get_context_data(self, **kwargs):
        context = super(PacienteCreate, self).get_context_data(**kwargs)
        context['PacienteForm'] = PacienteForm()
        return context

    def post(self, request, *args, **kwargs):

        persona_form = PersonaForm(data=self.request.POST)
        paciente_form = PacienteForm(data=self.request.POST)

        tipo = self.request.POST['tipo']
        nombre = self.request.POST['nombre']
        apellido = self.request.POST['apellido']

        tipo_documento = TipoDocumento.objects.filter(abreviatura='S/D')[0]

        if self.request.POST['numero_documento'] is '':
            mutable = self.request.POST._mutable
            self.request.POST._mutable = True
            self.request.POST['tipo_documento'] = tipo_documento.id
            self.request.POST._mutable = mutable

        if tipo == '':
            tipo = 1

        tipo_paciente = TipoPaciente.objects.get(pk=tipo)

        if tipo_paciente.valor == 'NORMAL':
            if nombre == "":
                messages.add_message(
                    request, messages.ERROR, 'DEBES INGRESAR EL NOMBRE - ')

            if apellido == "":
                messages.add_message(
                    request, messages.ERROR, 'DEBES INGRESAR EL APELLIDO - ')

        if persona_form.is_valid() and paciente_form.is_valid():
            persona = persona_form.save()
            paciente_form.instance.persona = persona
            paciente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'PACIENTE CREADO CON EXITO')

            return HttpResponseRedirect('/pacientes/modi/' + str(persona.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES.')

        return render_to_response(
            'pacientes/paciente_form.html',
            {'PacienteForm': paciente_form, 'form': persona_form},
            context_instance=RequestContext(request)
        )


class PacienteUpdate(UrlSessionMixin, UpdateView):

    model = Persona
    form_class = PersonaForm
    template_name = 'pacientes/paciente_form.html'
    modulo = 'pacientes'

    def get_context_data(self, **kwargs):
        context = super(PacienteUpdate, self).get_context_data(**kwargs)
        paciente = Paciente.objects.get(persona=self.object)
        context['PacienteForm'] = PacienteForm(instance=paciente)
        context['persona'] = self.object
        return context

    def post(self, request, *args, **kwargs):

        persona = Persona.objects.get(pk=kwargs['pk'])
        paciente = Paciente.objects.get(persona=persona)
        persona_form = PersonaForm(self.request.POST, instance=persona)
        paciente_form = PacienteForm(self.request.POST, instance=paciente)

        tipo_documento = TipoDocumento.objects.filter(abreviatura='S/D')[0]

        if self.request.POST['numero_documento'] is '':
            mutable = self.request.POST._mutable
            self.request.POST._mutable = True
            self.request.POST['tipo_documento'] = tipo_documento.id
            self.request.POST._mutable = mutable

        if persona_form.is_valid() and paciente_form.is_valid():
            persona = persona_form.save()
            paciente_form.instance.persona = persona
            paciente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'PACIENTE MODIFICADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'pacientes/paciente_form.html',
            {'PacienteForm': paciente_form, 'form': persona_form},
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class PacienteListView(ListView):
    model = Paciente
    paginate_by = 10

    def get_queryset(self):
        query = super(PacienteListView, self).get_queryset()

        parametro1 = self.request.GET.get('parametro1')
        parametro2 = self.request.GET.get('parametro2')

        if self.request.GET.get('combo_busqueda') == 'APELLIDO':
            query = self.buscar_por_apellido(parametro1)

        if self.request.GET.get('combo_busqueda') == 'NOMBRE':
            query = self.buscar_por_nombre(parametro1)

        if self.request.GET.get('combo_busqueda') == 'NUMERO_DOCUMENTO':
            query = self.buscar_por_numero_documento(
                parametro1)

        if self.request.GET.get('combo_busqueda') == 'CODIGO_PACIENTE':
            query = self.buscar_por_codigo_paciente(
                parametro1)

        if self.request.GET.get('combo_busqueda') == 'NOMBRE_APELLIDO':
            query = self.buscar_por_nombre_apellido(
                parametro1, parametro2)

        return query

    def buscar_por_apellido(self, apellido):
        paciente = Paciente.objects.filter(
            persona__apellido__icontains=apellido)

        return paciente

    def buscar_por_nombre(self, nombre):
        paciente = Paciente.objects.filter(persona__nombre__icontains=nombre)

        return paciente

    def buscar_por_numero_documento(self, numero):
        paciente = Paciente.objects.filter(
            persona__numero_documento__icontains=numero)

        return paciente

    def buscar_por_codigo_paciente(self, codigo):

        try:
            paciente = Paciente.objects.filter(pk__icontains=int(codigo))
        except:
            paciente = Paciente.objects.all()

        return paciente

    def buscar_por_nombre_apellido(self, nombre, apellido):
        paciente = Paciente.objects.filter(
            persona__nombre__icontains=nombre,
            persona__apellido__icontains=apellido)
        return paciente
