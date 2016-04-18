from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic import (TemplateView, CreateView, UpdateView,
                                  DeleteView)

from apps.complementos.locacion.models import LugarNacimiento
from apps.familiares.forms import (FamiliarForm, PersonaForm,
                                   FamiliarPacienteForm, LugarNacimientoForm)

from apps.familiares.models import Familiar, FamiliarPaciente
from apps.personas.models import Persona
from apps.pacientes.models import Paciente

from .setforms import SetMultipleFormsBuscar, SetMultipleFormsCreate
from . import helpers


class BusquedaFamiliarView(SetMultipleFormsBuscar, TemplateView):

    form_class = PersonaForm
    form_class_1 = FamiliarForm
    form_class_2 = LugarNacimientoForm
    form_class_3 = FamiliarPacienteForm

    template_name = 'familiares/familiar_form.html'
    mensaje = ('Rellene el campo N° de Documento para '
               'realizar una busqueda del familiar en '
               'caso de que exista')

    def post(self, request, *args, **kwargs):

        '''
        :param kwargs: id de el (**paciente)
        :return: envia de acuerdo al familiar existente a su respectiva vista
        '''

        persona = Persona.objects.filter(
            numero_documento=self.request.POST['numero_documento'])

        request.session['numero_documento_busqueda'] =\
            self.request.POST['numero_documento']

        if persona.exists() and self.request.POST['numero_documento'] is not '':
            return HttpResponseRedirect('/familiares/alta/' +
                                        str(self.kwargs['id']) +
                                        '/' + str(persona[0].id))
        else:
            return HttpResponseRedirect('/familiares/alta/' +
                                        str(self.kwargs['id']))


class FamiliarCreate(SetMultipleFormsCreate, CreateView):

    model = Familiar

    form_class = PersonaForm
    form_class_1 = FamiliarForm
    form_class_2 = LugarNacimientoForm
    form_class_3 = FamiliarPacienteForm

    template_name = 'familiares/familiar_form.html'
    success_url = 'familiares/busqueda/'
    mensaje = 'El familiar no existe, puede darlo de alta'

    def post(self, request, *args, **kwargs):

        paciente = Paciente.objects.get(persona__id=self.kwargs['id'])

        persona_form = PersonaForm(data=self.request.POST)
        familiar_form = FamiliarForm(data=self.request.POST)
        lugar_nacimiento_form = LugarNacimientoForm(data=self.request.POST)
        familiar_paciente_form = FamiliarPacienteForm(data=self.request.POST)

        if persona_form.is_valid() and familiar_form.is_valid() and \
                lugar_nacimiento_form.is_valid() and \
                familiar_paciente_form.is_valid():

            persona = persona_form.save()

            familiar_form.instance.persona = persona
            familiar = familiar_form.save()

            lugar_nacimiento_form.instance.persona = persona
            lugar_nacimiento_form.save()

            familiar_paciente_form.instance.paciente = paciente
            familiar_paciente_form.instance.familiar = familiar
            familiar_paciente_form.save()

            messages.add_message(request, messages.SUCCESS,
                                 'El familiar fue creado con éxito')

            return HttpResponseRedirect('/familiares/busqueda/' +
                                        str(paciente.persona.id))

        else:

            familiares_list = FamiliarPaciente.objects.filter(
                paciente=Paciente.objects.get(pk=paciente.id))

            return render_to_response('familiares/familiar_form.html',
                                      {
                                          'persona': paciente,
                                          'familiar_form': familiar_form,
                                          'familiares_list': familiares_list,
                                          'persona_form': persona_form,
                                          'familiar_paciente_form':
                                              familiar_paciente_form,
                                          'lugar_nacimiento_form':
                                              lugar_nacimiento_form
                                       },
                                      context_instance=RequestContext(request))


class FamiliarPacienteCreate(CreateView):

    model = Familiar
    form_class = FamiliarForm
    template_name = 'familiares/familiar_form.html'
    success_url = 'familiares/busqueda/'
    mensaje = 'Esta Persona ya se encuentra registrada'

    def get_context_data(self, **kwargs):

        context = super(FamiliarPacienteCreate, self).get_context_data(**kwargs)

        persona = Persona.objects.get(pk=self.kwargs['familiar'])

        persona_paciente = Persona.objects.get(pk=self.kwargs['id'])

        familiar = Familiar.objects.filter(persona__id=persona.id)

        familiares_list = FamiliarPaciente.objects.filter(
            paciente=Paciente.objects.get(persona=persona_paciente.id))

        if familiar.exists():
            lugar_nacimiento = LugarNacimiento.objects.get(
                persona__id=persona.id)

            familiar_form = FamiliarForm(
                initial={
                    'vive': familiar[0].vive,
                    'motivo_fallecimiento': familiar[0].motivo_fallecimiento,
                    'ocupacion': familiar[0].ocupacion,
                    'situacion_laboral': familiar[0].situacion_laboral,
                    'otra_ayuda_economica': familiar[0].otra_ayuda_economica,
                    'economicamente_activo': familiar[0].economicamente_activo
                })

            lugar_nacimiento_form = LugarNacimientoForm(
                initial={
                    'pais': lugar_nacimiento.pais,
                    'provincia': lugar_nacimiento.provincia,
                    'departamento': lugar_nacimiento.departamento
                })

            familiar_paciente_form = FamiliarPacienteForm()

        else:
            familiar_form = FamiliarForm()
            lugar_nacimiento_form = LugarNacimientoForm()
            familiar_paciente_form = FamiliarPacienteForm()

            context['familiar_form'] = familiar_form
            context['familiar_paciente_form'] = familiar_paciente_form
            context['lugar_nacimiento_form'] = lugar_nacimiento_form

        persona_form = PersonaForm(
            initial={
                'nombre': persona.nombre,
                'apellido': persona.apellido,
                'tipo_documento': persona.tipo_documento,
                'numero_documento': persona.numero_documento,
                'sexo': persona.sexo,
                'fecha_nacimiento': persona.fecha_nacimiento,
                'estado_civil': persona.estado_civil,
                'nivel_educacion': persona.nivel_educacion
            })

        context['persona_form'] = persona_form
        context['familiar_form'] = familiar_form
        context['familiar_paciente_form'] = familiar_paciente_form
        context['lugar_nacimiento_form'] = lugar_nacimiento_form
        context['familiares_list'] = familiares_list
        context['mensaje'] = self.mensaje

        return context

    def post(self, request, *args, **kwargs):

        persona_form = PersonaForm(data=self.request.POST)
        familiar_form = FamiliarForm(data=self.request.POST)
        lugar_nacimiento_form = LugarNacimientoForm(data=self.request.POST)
        familiar_paciente_form = FamiliarPacienteForm(data=self.request.POST)

        paciente = Paciente.objects.get(persona__id=self.kwargs['id'])
        persona = Persona.objects.get(pk=self.kwargs['familiar'])
        familiar = Familiar.objects.filter(persona__id=self.kwargs['familiar'])
        familiares_list = FamiliarPaciente.objects.filter(paciente=paciente)

        if familiar_form.is_valid() and \
                lugar_nacimiento_form.is_valid() and \
                familiar_paciente_form.is_valid():
            print('valida aca ')
            if familiar.exists() is False:
                familiar_form.instance.persona = persona
                familiar = familiar_form.save()

                lugar_nacimiento_form.instance.persona = persona
                lugar_nacimiento_form.save()
            else:
                familiar = familiar[0]

            familiar_paciente_form.instance.paciente = paciente
            familiar_paciente_form.instance.familiar = familiar

            familiar_paciente_form.save()

            messages.add_message(request, messages.SUCCESS,
                                 'El familiar fue creado con éxito')

            return HttpResponseRedirect('/familiares/busqueda/%s' %
                                        paciente.persona.id)
        else:

            messages.add_message(request, messages.ERROR,
                                 'El formulario contiene errores')

            return render_to_response('familiares/familiar_form.html',
                                      {'persona': paciente,
                                       'familiares_list': familiares_list,
                                       'familiar_form': familiar_form,
                                       'persona_form': persona_form,
                                       'familiar_paciente_form':
                                           familiar_paciente_form,
                                       'lugar_nacimiento_form':
                                           lugar_nacimiento_form},
                                      context_instance=RequestContext(request))


class FamiliarUpdate(UpdateView):

    model = FamiliarPaciente
    form_class = FamiliarForm
    template_name = 'familiares/familiar_form.html'

    def get_context_data(self, **kwargs):

        context = super(FamiliarUpdate, self).get_context_data(**kwargs)

        familiar_paciente = FamiliarPaciente.objects.get(pk=self.kwargs['pk'])
        familiar = Familiar.objects.get(pk=familiar_paciente.familiar.id)
        persona = Persona.objects.get(pk=familiar.persona.id)
        persona_paciente = Persona.objects.get(pk=self.kwargs['paciente'])

        helpers.guardar_variable_session_familiar(familiar.persona.id,
                                                  self.request)

        context['familiares_list'] = FamiliarPaciente.objects.filter(
            paciente=Paciente.objects.filter(persona=persona_paciente)[0])

        lugar_nacimiento = \
            LugarNacimiento.objects.filter(persona__id=persona.id)
        if lugar_nacimiento.exists():
            lugar_nacimiento = lugar_nacimiento[0]
            lugar_nacimiento_form = LugarNacimientoForm(instance=
                                                        lugar_nacimiento)
        else:
            lugar_nacimiento_form = LugarNacimientoForm()

        familiar_form = FamiliarForm(instance=familiar)
        familiar_paciente_form = FamiliarPacienteForm(
            instance=familiar_paciente)

        persona_form = PersonaForm(instance=persona)
        context['persona_form'] = persona_form
        context['familiar_form'] = familiar_form
        context['familiar_paciente_form'] = familiar_paciente_form
        context['lugar_nacimiento_form'] = lugar_nacimiento_form

        return context

    def post(self, request, *args, **kwargs):

        paciente_familiar = FamiliarPaciente.objects.get(pk=self.kwargs['pk'])
        familiar = Familiar.objects.get(pk=paciente_familiar.familiar.id)
        persona = Persona.objects.get(pk=familiar.persona.id)
        paciente = Paciente.objects.get(persona__id=self.kwargs['paciente'])

        familiar_form = FamiliarForm(instance=familiar, data=self.request.POST)
        persona_form = PersonaForm(instance=persona, data=self.request.POST)

        lugar_nacimiento = \
            LugarNacimiento.objects.get(persona__id=persona.id)
        if lugar_nacimiento:

            lugar_nacimiento_form = LugarNacimientoForm(instance=
                                                        lugar_nacimiento,
                                                        data=self.request.POST)
        else:
            lugar_nacimiento_form = LugarNacimientoForm(data=self.request.POST)

        familiar_paciente_form = FamiliarPacienteForm(instance=
                                                      paciente_familiar,
                                                      data=self.request.POST)

        if familiar_form.is_valid() and \
                lugar_nacimiento_form.is_valid() and \
                familiar_paciente_form.is_valid() and \
                persona_form.is_valid():

            persona = persona_form.save()
            familiar_form.instance.persona = persona
            lugar_nacimiento_form.instance.persona = persona

            familiar = familiar_form.save()
            lugar_nacimiento_form.save()

            familiar_paciente_form.instance.paciente = paciente
            familiar_paciente_form.instance.familiar = familiar

            familiar_paciente_form.save()

            messages.add_message(request, messages.SUCCESS,
                                 'El familiar fue modificado con éxito')

            return HttpResponseRedirect('/familiares/busqueda/%s' %
                                        paciente.persona.id)
        else:

            familiares_list = FamiliarPaciente.objects.filter(
                paciente=Paciente.objects.get(id=paciente.id))

            messages.add_message(request, messages.ERROR,
                                 'El formulario contiene errores')

            return render_to_response('familiares/familiar_form.html',
                                      {'persona': paciente,
                                       'familiares_list': familiares_list,
                                       'familiar_form': familiar_form,
                                       'familiar_paciente_form':
                                           familiar_paciente_form,
                                       'persona_form': persona_form,
                                       'lugar_nacimiento_form':
                                           lugar_nacimiento_form},
                                      context_instance=RequestContext(request))


class FamiliarDeleteView(DeleteView):
    model = FamiliarPaciente
    template_name = 'familiares/familiar_confirm_delete.html'

    def get_success_url(self):
        return '/familiares/busqueda/' + str(self.request.session['id'])
