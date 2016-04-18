
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, DeleteView

from . import helpers
from .forms import PersonaObraSocialForm
from .models import Persona, PersonaObraSocial


class PersonaObraSocialCreate(CreateView):
    model = PersonaObraSocial
    form_class = PersonaObraSocialForm

    def post(self, request, *args, **kwargs):
        persona = Persona.objects.get(pk=self.kwargs['id'])
        id_obrasocial = self.request.POST['obra_social']

        form = PersonaObraSocialForm(self.request.POST)

        if form.is_valid():
            if not helpers.existe_registro_persona_obra_social(persona, id_obrasocial):
                persona_obra_social = form.instance
                persona_obra_social.persona = persona
                persona_obra_social.save()
                messages.add_message(request, messages.SUCCESS,
                                     'OBRA SOCIAL REGISTRADA')
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'EL PACIENTE YA TIENE REGISTRADA ESTA OBRA SOCIAL'
                    )
                return HttpResponseRedirect('/obrassociales/alta/' + str(persona.id))

        messages.add_message(request, messages.ERROR,
                             'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'personas/personaobrasocial_form.html',
            {'form': form},
            context_instance=RequestContext(request)
            )

    def get_context_data(self, **kwargs):
        context = super(
            PersonaObraSocialCreate, self).get_context_data(**kwargs)
        context['obrasocial_list'] = PersonaObraSocial.objects.filter(
            persona__id=self.kwargs['id'])
        context['persona_list'] = Persona.objects.filter(
            pk=self.kwargs['id'])
        return context

    def get_success_url(self):
        return self.request.get_full_path()


class PersonaObraSocialUpdate(UpdateView):

    model = PersonaObraSocial
    form_class = PersonaObraSocialForm

    def post(self, request, *args, **kwargs):
        persona_obra_social = PersonaObraSocial.objects.get(pk=kwargs['pk'])
        persona = str(persona_obra_social.persona.id)
        id_obrasocial = self.request.POST['obra_social']
        persona_obra_social_actualiza = PersonaObraSocialForm(
            self.request.POST, instance=persona_obra_social)

        if persona_obra_social_actualiza.is_valid():
            if not helpers.existe_registro_persona_obra_social_update(
                persona, id_obrasocial):

                persona_obra_social_actualiza.instance
                persona_obra_social_actualiza.save()
                messages.add_message(request, messages.SUCCESS,
                                     'LA OBRA SOCIAL SE MODIFICO CON ÉXITO')
                return HttpResponseRedirect(
                    '/obrassociales/alta/' + str(persona))
            else:
                messages.add_message(
                        request, messages.ERROR,
                        'EL PACIENTE YA TIENE REGISTRADA ESTA OBRA SOCIAL'
                        )
                return HttpResponseRedirect(
                    '/obrassociales/modi/' + str(persona_obra_social.pk))

        messages.add_message(request, messages.ERROR,
                             'EL FORMULARIO CONTIENE ERROES')

        return render_to_response(
            'personas/personaobrasocial_form.html',
            {'form': persona_obra_social_actualiza},
            context_instance=RequestContext(request)
            )

    def dispatch(self, *args, **kwargs):
        id_persona = PersonaObraSocial.objects.filter(
            id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(PersonaObraSocialUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            PersonaObraSocialUpdate, self).get_context_data(**kwargs)
        context['obrasocial_list'] = PersonaObraSocial.objects.filter(
            persona=self.kwargs['pk'])
        #context['persona_list'] = Persona.objects.filter(pk=self.kwargs['pk'])
        context['persona_list'] = Persona.objects.filter(pk=self.persona.id)
        return context

    def get_success_url(self):
        return self.request.get_full_path()


class PersonaObraSocialDelete(DeleteView):

    model = PersonaObraSocial

    def dispatch(self, *args, **kwargs):
        id_persona = PersonaObraSocial.objects.filter(
            id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(PersonaObraSocialDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/obrassociales/alta/' + str(self.persona.id)
