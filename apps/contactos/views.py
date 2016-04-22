from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import render_to_response

from .models import Contacto
from apps.clientes.models import Cliente

from .forms import ContactoForm


class ContactoCreate(SuccessMessageMixin, CreateView):

    model = Contacto
    form_class = ContactoForm

    def get(self, request, *args, **kwargs):

        form = ContactoForm()

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        contactos_list = Contacto.objects.filter(persona_id=cliente.persona.id)

        return render_to_response(
            'contactos/contacto_form.html',
            {
                'form': form,
                'cliente': cliente,
                'contactos_list': contactos_list
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        print(self.request.POST)

        form = ContactoForm(data=self.request.POST)

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        contactos_list = cliente.persona.contacto_set.all()

        if form.is_valid():

            form.save()

            messages.add_message(
                request, messages.SUCCESS,
                'CONTACTO CREADO CON EXITO')

            return HttpResponseRedirect('/contactos/alta/' + str(cliente.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'contactos/contacto_form.html',
            {
                'form': form,
                'cliente': cliente,
                'contactos_list': contactos_list
            },
            context_instance=RequestContext(request)
        )


class ContactoDelete(DeleteView):

    model = Contacto
    success_message = 'El contacto fue eliminado con éxito'

    def get_success_url(self):
        cliente = Cliente.objects.get(pk=self.kwargs['pk'])

        return '/contactos/alta/' + str(cliente.id)


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
