
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)

from .forms import EntidadForm
from .models import Entidad
from . import helpers


class EntidadListView(ListView):
    model = Entidad
    paginate_by = 10

    def get_queryset(self):

        query = super(EntidadListView, self).get_queryset()

        # parametro = self.request.GET.get('parametro')
        #
        # print(parametro)
        #
        # if parametro:
        #
        #     query = Entidad.objects.filter(
        #         Q(persona__apellido__icontains=parametro) |
        #         Q(persona__nombre__icontains=parametro) |
        #         Q(persona__numero_documento__icontains=parametro)
        #     )

        return query


class EntidadCreate(CreateView):
    model = Entidad
    form_class = EntidadForm

    def get(self, request, *args, **kwargs):

        form = EntidadForm()

        return render_to_response(
            'organigrama/entidad_form.html', {'form': form},
            context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):

        form = EntidadForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            form_entidad = form.save(commit=False)

            if 'imagen' in self.request.FILES:
                self.set_foto(form_entidad, (self.request.FILES['imagen']))

            form_entidad.save()

            messages.add_message(
                request, messages.SUCCESS, 'ENTIDAD CREADA CON EXITO')

            return HttpResponseRedirect('/entidades/modi/%s' %
                                        str(form_entidad.id))

        messages.add_message(
            request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'organigrama/entidad_form.html', {'form': form},
            context_instance=RequestContext(request))

    def set_foto(self, entidad, foto):
        '''
        foto.name = helpers.cambiar_nombre_imagen(
            foto.name, int(Persona.objects.latest('id').id) + 1)
        '''

        entidad_nombre = self.request.POST['nombre']

        foto.name = helpers.cambiar_nombre_imagen(foto.name, entidad_nombre)

        foto = helpers.redimensionar_imagen(entidad.imagen, foto.name)
        # Se envia foto subida y el cambio de nombre, como parametros
        entidad.foto = foto

    def get_success_url(self):
        return self.request.get_full_path()


class EntidadUpdate(UpdateView):
    model = Entidad
    form_class = EntidadForm

    def get(self, request, *args, **kwargs):

        entidad = Entidad.objects.get(pk=kwargs['pk'])
        form = EntidadForm(instance=entidad)

        return render_to_response('organigrama/entidad_form.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        pass
    #     cliente = Cliente.objects.get(pk=kwargs['pk'])
    #     persona = Persona.objects.get(pk=cliente.persona.id)
    #
    #     persona_form = PersonaForm(self.request.POST, self.request.FILES,
    #                                instance=persona)
    #     cliente_form = ClienteForm(self.request.POST, instance=cliente)
    #
    #     if persona_form.is_valid() and cliente_form.is_valid():
    #
    #         if 'foto' in self.request.FILES:
    #             self.set_foto(persona_form, self.request.FILES['foto'])
    #
    #         persona = persona_form.save()
    #         cliente_form.instance.persona = persona
    #
    #         cliente_form.save()
    #
    #         messages.add_message(
    #             request, messages.SUCCESS, 'CLIENTE MODIFICADO CON EXITO')
    #
    #         return HttpResponseRedirect('/clientes/modi/%s' % kwargs['pk'])
    #
    #     messages.add_message(
    #         request, messages.SUCCESS, 'EL FORMULARIO CONTIENE ERRORES')
    #
    #     return render_to_response(
    #         'organigrama/entidad_form.html',
    #         {
    #             'form': persona_form,
    #             'cliente_form': cliente_form
    #         },
    #         context_instance=RequestContext(request)
    #     )
    #
    # def set_foto(self, persona, foto):
    #     foto.name = \
    #         helpers.cambiar_nombre_imagen(foto.name, persona.instance.id)
    #     persona.instance.foto = helpers.redimensionar_imagen(
    #         persona.instance.foto, foto.name)
    #     persona.save()
    #
    # def get_success_url(self):
    #     return self.request.get_full_path()


class EntidadDelete(DeleteView):
    model = Entidad

    def get_success_url(self):
        return '/entidades/listado/'