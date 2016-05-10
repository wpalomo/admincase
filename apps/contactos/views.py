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

        # contactos_list = Contacto.objects.filter(persona_id=cliente.persona.id)
        contactos_list = cliente.persona.contacto_set.all()

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


class ContactoUpdate(SuccessMessageMixin, UpdateView):

    model = Contacto
    form_class = ContactoForm

    def get(self, request, *args, **kwargs):

        contacto = Contacto.objects.get(pk=kwargs['pk'])

        form = ContactoForm(instance=contacto)

        cliente = contacto.persona.cliente

        contactos_list = contacto.persona.contacto_set.all()

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

        contacto = Contacto.objects.get(pk=kwargs['pk'])

        cliente = contacto.persona.cliente

        form = ContactoForm(self.request.POST, instance=contacto)

        contactos_list = contacto.persona.contacto_set.all()

        if form.is_valid():

            form.save()

            messages.add_message(
                request, messages.SUCCESS, 'CONTACTO MODIFICADO CON EXITO')

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

    def get_success_url(self):
        contacto = Contacto.objects.get(pk=self.kwargs['pk'])

        messages.add_message(
            self.request, messages.SUCCESS, 'EL CONTACTO FUE ELIMINADO CON ÉXITO')

        return '/contactos/alta/' + str(contacto.persona.cliente.id)