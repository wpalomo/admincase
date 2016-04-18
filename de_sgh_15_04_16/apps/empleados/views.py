# -*- encoding: utf-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from apps.personas.mixins import UrlSessionMixin
from apps.personas.models import Persona

from .import helpers
from .forms import PersonaForm, EmpleadoForm, AsignacionFormalForm
from .models import Empleado, AsignacionFormal


class EmpleadoCreate(CreateView):

    model = Empleado
    form_class = PersonaForm

    def get_context_data(self, **kwargs):
        context = super(EmpleadoCreate, self).get_context_data(**kwargs)
        context['empleado_form'] = EmpleadoForm()
        return context

    def post(self, request, *args, **kwargs):
        persona_form = PersonaForm(self.request.POST, self.request.FILES)
        empleado_form = EmpleadoForm(data=self.request.POST)

        if persona_form.is_valid() and empleado_form.is_valid():
            persona = persona_form.save(commit=False)

            if 'foto' in self.request.FILES:
                self.set_foto(persona, (self.request.FILES['foto']))
            persona.save()
            empleado_form.instance.persona = persona
            empleado_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'EMPLEADO CREADO CON EXITO')

            return HttpResponseRedirect('/empleados/modi/%s' % str(persona.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'empleados/empleado_form.html',
            {'empleado_form': empleado_form, 'form': persona_form},
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


class EmpleadoUpdate(UrlSessionMixin, UpdateView):

    model = Persona
    form_class = PersonaForm
    template_name = 'empleados/empleado_form.html'
    modulo = 'empleados'

    def get_context_data(self, **kwargs):
        context = super(EmpleadoUpdate, self).get_context_data(**kwargs)
        empleado = Empleado.objects.get(persona=self.object)
        context['empleado_form'] = EmpleadoForm(instance=empleado)
        context['persona'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        persona = Persona.objects.get(pk=kwargs['pk'])
        empleado = Empleado.objects.get(persona=persona)
        persona_form = PersonaForm(self.request.POST, self.request.FILES,
                                   instance=persona)
        empleado_form = EmpleadoForm(self.request.POST, instance=empleado)

        if persona_form.is_valid() and empleado_form.is_valid():

            if 'foto' in self.request.FILES:
                self.set_foto(persona_form, self.request.FILES['foto'])

            persona = persona_form.save()
            empleado_form.instance.persona = persona

            empleado_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'EMPLEADO MODIFICADO CON EXITO')

            return HttpResponseRedirect('/empleados/modi/%s' % kwargs['pk'])

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'empleados/empleado_form.html',
            {'empleado_form': empleado_form, 'form': persona_form},
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


class EmpleadoListView(ListView):

    model = Empleado
    paginate_by = 20
    # queryset = Empleado.objects.order_by('persona__apellido')

    def get_queryset(self):

        query = super(EmpleadoListView, self).get_queryset()

        parametro1 = self.request.GET.get('parametro1')
        parametro2 = self.request.GET.get('parametro2')

        if self.request.GET.get('filtro') == 'APELLIDO':
            query = self.buscar_por_apellido(parametro1)

        if self.request.GET.get('filtro') == 'NOMBRE':
            query = self.buscar_por_nombre(parametro1)

        if self.request.GET.get('filtro') == 'NUMERO_DOCUMENTO':
            query = self.buscar_por_numero_documento(parametro1)

        if self.request.GET.get('filtro') == 'PROFESION':
            query = self.buscar_por_profesion(parametro1)

        if self.request.GET.get('filtro') == 'FECHA_INGRESO':
            query = self.buscar_por_fecha_ingreso(parametro1, parametro2)

        if self.request.GET.get('filtro') == 'FECHA_EGRESO':
            query = self.buscar_por_fecha_egreso(parametro1, parametro2)

        if self.request.GET.get('filtro') == 'FECHA_NACIMIENTO':
            query = self.buscar_por_fecha_nacimiento(parametro1)

        return query

    def buscar_por_apellido(self, apellido):
        empleado = Empleado.objects.filter(
            persona__apellido__icontains=apellido).order_by('persona__apellido')

        return empleado

    def buscar_por_nombre(self, nombre):
        empleado = Empleado.objects.filter(
            persona__nombre__icontains=nombre).order_by('persona__apellido')

        return empleado

    def buscar_por_numero_documento(self, numero):
        empleado = Empleado.objects.filter(
            persona__numero_documento__icontains=numero).order_by('persona__apellido')

        return empleado

    def buscar_por_profesion(self, profesion):
        empleado = Empleado.objects.filter(
            persona__profesion__nombre__icontains=profesion).order_by('persona__apellido')

        return empleado

    def buscar_por_fecha_ingreso(self, fecha_desde, fecha_hasta):

        fecha_desde = fecha_desde.strip()
        fecha_hasta = fecha_hasta.strip()

        try:
            fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y')
        except ValueError:
            fecha_desde = datetime.now()

        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y')
        except ValueError:
            fecha_hasta = datetime.now()

        empleados = Empleado.objects.filter(
            fecha_ingreso__range=[fecha_desde, fecha_hasta]).order_by('persona__apellido')

        return empleados

    def buscar_por_fecha_egreso(self, fecha_desde, fecha_hasta):

        fecha_desde = fecha_desde.strip()
        fecha_hasta = fecha_hasta.strip()

        try:
            fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y')
        except ValueError:
            fecha_desde = datetime.now()

        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y')
        except ValueError:
            fecha_hasta = datetime.now()

        empleados = Empleado.objects.filter(
            fecha_egreso__range=[fecha_desde, fecha_hasta]).order_by('persona__apellido')

        return empleados

    def buscar_por_fecha_nacimiento(self, fecha):
        empleados = Empleado.objects.filter(
            persona__profesion__fecha_nacimiento__icontains=fecha).order_by('persona__apellido')

        return empleados


class AuditoriaList(ListView):
    model = LogEntry
    template_name = "auditoria_list.html"
    paginate_by = 10


class AsignacionFormalCreate(CreateView):

    model = AsignacionFormal
    form_class = AsignacionFormalForm

    def get(self, request, *args, **kwargs):

        form = AsignacionFormalForm()

        empleado = Empleado.objects.get(pk=kwargs['pk'])

        asignaciones_formales = AsignacionFormal.objects.filter(
            empleado_id=kwargs['pk'])

        return render_to_response(
            'empleados/asignacionformal_form.html',
            {
                'form': form,
                'empleado': empleado,
                'asignaciones_formales_list': asignaciones_formales
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = AsignacionFormalForm(data=self.request.POST)

        empleado = Empleado.objects.get(pk=kwargs['pk'])

        asignaciones_formales = AsignacionFormal.objects.filter(
            empleado_id=kwargs['pk'])

        if form.is_valid():

            asignacion_formal = form.save()

            messages.add_message(
                request, messages.SUCCESS,
                'ASIGANCION FORMAL DEL EMPLEADO CREADO CON EXITO')

            return HttpResponseRedirect(
                '/empleados/asignacionformal/alta/'
                + str(asignacion_formal.empleado.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'empleados/asignacionformal_form.html',
            {
                'form': form,
                'empleado': empleado,
                'asignaciones_formales_list': asignaciones_formales
            },
            context_instance=RequestContext(request)
        )


class AsignacionFormalUpdate(UpdateView):

    model = AsignacionFormal
    form_class = AsignacionFormalForm

    def get(self, request, *args, **kwargs):

        asignacion_formal = AsignacionFormal.objects.get(pk=kwargs['pk'])

        empleado = Empleado.objects.get(pk=asignacion_formal.empleado.id)

        form = AsignacionFormalForm(instance=asignacion_formal)

        asignaciones_formales = empleado.asignacionformal_set.all()

        return render_to_response(
            'empleados/asignacionformal_form.html',
            {
                'form': form,
                'empleado': empleado,
                'asignaciones_formales_list': asignaciones_formales
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        asignacion_formal = AsignacionFormal.objects.get(pk=kwargs['pk'])
        empleado = Empleado.objects.get(pk=asignacion_formal.empleado.id)

        form = AsignacionFormalForm(
            data=self.request.POST, instance=asignacion_formal)

        asignaciones_formales = empleado.asignacionformal_set.all()

        if form.is_valid():

            asignacion_formal = form.save()

            messages.add_message(
                request, messages.SUCCESS,
                'ASIGANCION FORMAL DEL EMPLEADO MODIFICADO CON EXITO')

            return HttpResponseRedirect(
                '/empleados/asignacionformal/alta/'
                + str(asignacion_formal.empleado.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'empleados/asignacionformal_form.html',
            {
                'form': form,
                'empleado': empleado,
                'asignaciones_formales_list': asignaciones_formales
            },
            context_instance=RequestContext(request)
        )


class AsignacionFormalDelete(DeleteView):

    model = AsignacionFormal

    def get_success_url(self):
        asignacion_formal = AsignacionFormal.objects.get(pk=self.kwargs['pk'])

        return '/empleados/asignacionformal/alta/' + \
               str(asignacion_formal.empleado.id)