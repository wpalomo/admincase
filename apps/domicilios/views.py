
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from apps.personas.models import Persona

from .forms import DomicilioForm
from .models import Domicilio


class DomicilioUpdate(UpdateView):

    model = Domicilio
    form_class = DomicilioForm

    def get_context_data(self, **kwargs):
        context = super(DomicilioUpdate, self).get_context_data(**kwargs)
        path = self.request.get_full_path()
        context['modulo'] = self.get_modulo(path)
        return context

    def dispatch(self, *args, **kwargs):
        id_persona = Domicilio.objects.filter(id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(DomicilioUpdate, self).dispatch(*args, **kwargs)

    def get_modulo(self, path):
        modulo = path.split('/')[2]
        return modulo

    def get_success_url(self):
        return '/domicilios/alta/%s' % str(self.persona.id)

    def get_context_data(self, **kwargs):
        context = super(DomicilioUpdate, self).get_context_data(**kwargs)
        context['list'] = Domicilio.objects.filter(persona=self.persona)
        return context


class DomicilioCreate(SuccessMessageMixin, CreateView):

    model = Domicilio
    template_name = 'domicilios/domicilio_form.html'
    success_url = '/domicilio/crear/'
    form_class = DomicilioForm
    success_message = 'El domicilio se registro con exito'

    def form_valid(self, form):
        form.instance.persona = self.persona
        return super(DomicilioCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.persona = Persona.objects.get(pk=kwargs['id'])
        return super(DomicilioCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/domicilios/alta/%s' % str(self.persona.id)

    def get_context_data(self, **kwargs):
        context = super(DomicilioCreate, self).get_context_data(**kwargs)
        context['list'] = Domicilio.objects.filter(persona=self.persona)
        return context


class DomicilioDelete(DeleteView):

    model = Domicilio
    template_name = 'domicilios/domicilio_delete_confirm.html'

    def dispatch(self, *args, **kwargs):
        id_persona = Domicilio.objects.filter(id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(DomicilioDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/domicilios/alta/%s' % str(self.persona.id)