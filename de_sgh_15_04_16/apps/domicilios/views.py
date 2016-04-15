
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.utils import ErrorList
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.personas.models import Persona
from apps.familiares.models import Familiar

from .forms import DomicilioForm
from .models import Domicilio
from apps.pacientes.models import Paciente


class DomicilioUpdate(SuccessMessageMixin, UpdateView):

    model = Domicilio
    form_class = DomicilioForm
    success_message = 'El domicilio se modifico con éxito'

    def dispatch(self, *args, **kwargs):
        id_persona = Domicilio.objects.filter(
            id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)

        return super(DomicilioUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomicilioUpdate, self).get_context_data(**kwargs)
        context['domicilio_list'] = Domicilio.objects.filter(
            persona=self.persona)
        context['persona_list'] = Persona.objects.filter(pk=self.persona.id)
        return context

    def get_success_url(self):
        return '/domicilios/alta/%s' % str(self.persona.id)


class DomicilioCreate(SuccessMessageMixin, CreateView):

    model = Domicilio
    template_name = 'domicilios/domicilio_form.html'
    success_url = '/domicilio/crear/'
    form_class = DomicilioForm
    success_message = 'El domicilio se registro con exito'

    def dispatch(self, *args, **kwargs):
        self.persona = Persona.objects.get(pk=kwargs['id'])
        return super(DomicilioCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DomicilioCreate, self).get_context_data(**kwargs)
        context['domicilio_list'] = Domicilio.objects.filter(
            persona=self.persona)
        context['persona_list'] = Persona.objects.filter(pk=self.persona.id)
        #
        # if self.request.session['modulo'] == '':
        #     paciente = Paciente.objects.filter(persona__id=self.persona.id)
        #     if paciente.exists():
        #         familiar = Familiar.objects.filter(persona__id=self.persona.id)
        #         if familiar.exists():
        #             self.request.session['modulo_titulo'] = ' '
        #         else:
        #             self.request.session['modulo_titulo'] = 'pacientes'

        return context

    def form_valid(self, form):
        form.instance.persona = self.persona
        return super(DomicilioCreate, self).form_valid(form)

    def get_success_url(self):
        return '/domicilios/alta/' + str(self.persona.id)


class DomicilioDelete(DeleteView):

    model = Domicilio
    template_name = 'domicilios/domicilio_delete_confirm.html'

    def dispatch(self, *args, **kwargs):
        id_persona = Domicilio.objects.filter(id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(DomicilioDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/domicilios/alta/' + str(self.persona.id)
