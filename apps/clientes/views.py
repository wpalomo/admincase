
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.personas.models import Persona

from .forms import PersonaForm, ClienteForm
from .models import Cliente


class ClienteListView(ListView):
    model = Cliente
    paginate_by = 10


class ClienteCreate(CreateView):
    model = Cliente
    form_class = PersonaForm

    def get_context_data(self, **kwargs):
        context = super(ClienteCreate, self).get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm()
        return context

    def post(self, request, *args, **kwargs):

        persona_form = PersonaForm(data=self.request.POST)
        cliente_form = ClienteForm(data=self.request.POST)

        if persona_form.is_valid() and cliente_form.is_valid():
            persona = persona_form.save()
            cliente_form.instance.persona = persona
            cliente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'CLIENTE CREADO CON EXITO')

            return HttpResponseRedirect('/clientes/modi/%s' % str(persona.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'cliente_form': cliente_form,
                'form': persona_form
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteUpdate(UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'clientes/cliente_form.html'
    # modulo = 'clientes'

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdate, self).get_context_data(**kwargs)
        cliente = Cliente.objects.get(persona=self.object)
        context['cliente_form'] = ClienteForm(instance=cliente)
        context['persona'] = self.object
        return context

    def post(self, request, *args, **kwargs):

        persona = Persona.objects.get(pk=kwargs['pk'])
        cliente = Cliente.objects.get(persona=persona)

        persona_form = PersonaForm(self.request.POST, instance=persona)
        cliente_form = ClienteForm(self.request.POST, instance=cliente)

        if persona_form.is_valid() and cliente_form.is_valid():
            persona = persona_form.save()
            cliente_form.instance.persona = persona
            cliente_form.save()

            messages.add_message(
                request, messages.SUCCESS, 'CLIENTE MODIFICADO CON EXITO')

            return HttpResponseRedirect('/clientes/modi/%s' % kwargs['pk'])

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'clientes/cliente_form.html',
            {
                'cliente_form': cliente_form,
                'form': persona_form
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class ClienteDelete(DeleteView):
    model = Cliente