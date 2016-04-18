from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from .models import Nota
from .forms import NotaForm
from apps.personas.models import Persona


class NotaCreate(SuccessMessageMixin, CreateView):

    model = Nota
    form_class = NotaForm
    success_message = 'La nota se guardo con éxito'

    def dispatch(self, *args, **kwargs):
        self.persona = Persona.objects.get(pk=kwargs['id'])
        return super(NotaCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(NotaCreate, self).get_context_data(**kwargs)
        context['notas_list'] = Nota.objects.filter(
            persona=self.persona).order_by('-fecha')
        context['persona_list'] = Persona.objects.filter(pk=self.persona.id)
        return context

    def form_valid(self, form):
        form.instance.persona = self.persona
        usuario = User.objects.get(username=self.request.user.username)
        form.instance.usuario = usuario
        form.save()
        return super(NotaCreate, self).form_valid(form)

    def get_success_url(self):
        return '/notas/alta/' + str(self.persona.id)


class NotaUpdate(SuccessMessageMixin, UpdateView):

    model = Nota
    success_message = 'La nota se modifico con éxito'
    success_url = '/notas/alta/'
    form_class = NotaForm

    def dispatch(self, *args, **kwargs):
        id_persona = Nota.objects.filter(
            id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(NotaUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotaUpdate, self).get_context_data(**kwargs)
        context['notas_list'] = Nota.objects.filter(
            persona=self.persona).order_by('-fecha')
        context['persona_list'] = Persona.objects.filter(pk=self.persona.id)
        return context

    def form_valid(self, form):
        form.instance.persona = self.persona
        usuario = User.objects.get(username=self.request.user.username)
        form.instance.usuario = usuario
        form.save()
        return super(NotaUpdate, self).form_valid(form)

    def get_success_url(self):
        return '/notas/alta/' + str(self.persona.id)


class NotaDelete(DeleteView):

    model = Nota
    success_message = 'La nota fue eliminada con éxito'

    def dispatch(self, *args, **kwargs):
        id_persona = Nota.objects.filter(id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(NotaDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/notas/alta/' + str(self.persona.id)

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(NotaDelete, self).delete(request, *args, **kwargs)
