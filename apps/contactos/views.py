from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Contacto
from apps.clientes.models import Cliente

from .forms import ContactoForm


class ContactoCreate(SuccessMessageMixin, CreateView):

    model = Contacto
    form_class = ContactoForm
    success_url = '/contacto/listado/'
    success_message = 'El contacto se creo de forma correcta'

    def dispatch(self, *args, **kwargs):
        self.cliente = Cliente.objects.get(pk=kwargs['id'])
        return super(ContactoCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactoCreate, self).get_context_data(**kwargs)
        context['contacto_list'] = Contacto.objects.filter(
            persona=self.cliente.persona)
        context['persona_list'] = Cliente.objects.filter(
            pk=self.cliente.persona.id)

        return context

    def form_valid(self, form):
        form.instance.persona = self.persona

        return super(ContactoCreate, self).form_valid(form)

    def get_success_url(self):
        return '/contactos/alta/' + str(self.persona.id)


class ContactoDelete(DeleteView):

    model = Contacto
    success_message = 'El contacto fue eliminado con éxito'

    def dispatch(self, *args, **kwargs):
        id_persona = Contacto.objects.filter(id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(ContactoDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return '/contactos/alta/' + str(self.persona.id)

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(ContactoDelete, self).delete(request, *args, **kwargs)


class ContactoUpdate(SuccessMessageMixin, UpdateView):

    model = Contacto
    success_message = 'El contacto se modifico con éxito'
    success_url = '/contactos/alta/'
    form_class = ContactoForm

    def dispatch(self, *args, **kwargs):
        id_persona = Contacto.objects.filter(
            id=kwargs['pk']).values('persona')
        self.persona = Persona.objects.get(pk=id_persona)
        return super(ContactoUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactoUpdate, self).get_context_data(**kwargs)
        context['contacto_list'] = Contacto.objects.filter(
            persona=self.persona)
        context['persona_list'] = Persona.objects.filter(
            pk=self.persona.id)
        return context

    def form_valid(self, form):
        form.instance.persona = self.persona
        return super(ContactoUpdate, self).form_valid(form)

    def get_success_url(self):
        return '/contactos/alta/' + str(self.persona.id)
