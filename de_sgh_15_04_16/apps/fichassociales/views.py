
import datetime

from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import FichaSocial
from apps.pacientes.models import Paciente
from apps.personas.models import Persona, PersonaObraSocial

from .forms import FichaSocialForm, PersonaForm, PacienteForm


class FichaSocialCreate(SuccessMessageMixin, CreateView):
    model = FichaSocial
    form_class = FichaSocialForm
    template_name = 'fichassociales/fichasocial_form.html'
    success_message = 'La ficha Social se registro con exito'

    def get_context_data(self, **kwargs):
        context = super(FichaSocialCreate, self).get_context_data(**kwargs)

        persona = Persona.objects.get(pk=self.kwargs['id'])
        paciente = Paciente.objects.get(persona=persona)

        context['persona_form'] = PersonaForm(instance=persona)
        context['paciente_form'] = PacienteForm(instance=paciente)
        context['persona_obra_social'] = PersonaObraSocial.objects.filter(
            persona=persona, habitual=True)
        context['persona'] = persona
        return context

    def post(self, request, *args, **kwargs):

        if 'verificar' in self.request.POST:

            request.POST._mutable = True
            request.POST['ultima_verificacion'] = datetime.datetime.now()
            request.POST._mutable = False

        ficha_social_form = FichaSocialForm(data=self.request.POST)
        persona = Persona.objects.get(pk=self.kwargs['id'])

        paciente = Paciente.objects.get(persona=persona)
        persona_form = PersonaForm(instance=persona, data=self.request.POST)
        paciente_form = PacienteForm(instance=paciente, data=self.request.POST)
        persona_obra_social = PersonaObraSocial.objects.filter(persona=persona)

        if ficha_social_form.is_valid() and persona_form.is_valid():

            if persona_obra_social.exists() is False:
                messages.add_message(
                    request, messages.ERROR,
                    'EL PACIENTE NO TIENE OBRA SOCIAL HABITUAL ASIGNADA.'
                    'ACTUALICE ESTE ITEM ANTES DE VERIFICAR LA FICHA'
                    )
                return HttpResponseRedirect('/obrassociales/alta/' + str(
                    persona.id))

            persona = persona_form.save()
            paciente_form.save()
            paciente = Paciente.objects.get(persona__id=persona.id)
            ficha_social_form.instance.paciente = paciente
            ficha_social_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'FICHA SOCIAL CREADA CON ÉXITO')

            return HttpResponseRedirect('/fichassociales/modi/' + str(
                persona.id) + "/" + str(ficha_social_form.instance.id))

        else:
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
             'fichassociales/fichasocial_form.html',
             {'persona_form': persona_form,
              'form': ficha_social_form,
              'paciente_form': paciente_form,
              'persona_obra_social': persona_obra_social},
             context_instance=RequestContext(request)
             )


class FichaSocialUpdate(SuccessMessageMixin, UpdateView):

    model = FichaSocial
    form_class = FichaSocialForm
    template_name = 'fichassociales/fichasocial_form.html'
    succes_message = 'La Ficha Social se ha modificado con exito'

    def get_context_data(self, **kwargs):
        context = super(FichaSocialUpdate, self).get_context_data(**kwargs)
        # Se filtra la persona,
        # para enviar sus datos dentro de la ficha social
        persona = Persona.objects.get(pk=self.kwargs['id'])
        paciente = Paciente.objects.get(persona=persona)
        context['persona_form'] = PersonaForm(instance=persona)
        context['paciente_form'] = PacienteForm(instance=paciente)
        context['persona_obra_social'] = PersonaObraSocial.objects.filter(
            persona=persona, habitual=True)
        context['persona'] = persona
        return context

    def post(self, request, *args, **kwargs):

        ficha_social = FichaSocial.objects.get(pk=self.kwargs['pk'])
        persona = Persona.objects.get(pk=self.kwargs['id'])
        paciente = Paciente.objects.get(persona=persona)
        persona_obra_social = PersonaObraSocial.objects.filter(
            persona=persona, habitual=True)

        if 'verificar' in self.request.POST:

            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['ultima_verificacion'] = datetime.datetime.now()
            request.POST._mutable = mutable

        ficha_social_form = FichaSocialForm(instance=ficha_social,
                                            data=self.request.POST)
        persona = Persona.objects.get(pk=self.kwargs['id'])
        # Se instancia la persona para
        # no repetir sus datos ya cargados
        persona_form = PersonaForm(instance=persona, data=self.request.POST)
        paciente_form = PacienteForm(instance=paciente, data=self.request.POST)

        if ficha_social_form.is_valid() and persona_form.is_valid():
            if persona_obra_social.exists() is False:
                messages.add_message(
                    request, messages.ERROR,
                    'EL PACIENTE NO TIENE OBRA SOCIAL HABITUAL ASIGNADA.'
                    'ACTUALICE ESTE ITEM ANTES DE VERIFICAR LA FICHA')
                return HttpResponseRedirect('/obrassociales/alta/' + str(
                    persona.id))

            persona = persona_form.save()
            paciente = Paciente.objects.get(persona__id=persona.id)
            ficha_social_form.instance.paciente = paciente
            paciente_form.save()
            ficha_social_form.save()

            messages.add_message(
                request, messages.SUCCESS,
                'FICHA SOCIAL MODIFICADA CON ÉXITO')

            return HttpResponseRedirect('/fichassociales/modi/' + str(
                persona.id) + '/' + str(ficha_social.id))
        else:
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
             'fichassociales/fichasocial_form.html',
             {'persona_form': persona_form,
              'form': ficha_social_form,
              'paciente_form': paciente_form,
              'persona_obra_social': persona_obra_social},
             context_instance=RequestContext(request)
             )


def redireccionar_ficha(self, *args, **kwargs):
    '''
    :param kwargs: devuelve el id de la persona
    :return: Redirecciona a un UpdateView
    en caso de que la ficha social ya exista
    '''

    paciente = Paciente.objects.get(persona__id=kwargs['id'])

    ficha_social = FichaSocial.objects.filter(paciente=paciente)

    if ficha_social.exists():
        return HttpResponseRedirect('/fichassociales/modi/' + str(
                 paciente.persona.id) + "/" + str(ficha_social[0].id))
    else:
        return HttpResponseRedirect('/fichassociales/alta/' + str(
                  paciente.persona.id))
