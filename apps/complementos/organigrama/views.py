
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
            # form_entidad = form.save(commit=False)

            if 'imagen' in self.request.FILES:
                self.set_foto(form, (self.request.FILES['imagen']))

            form.save()

            messages.add_message(
                request, messages.SUCCESS, 'ENTIDAD CREADA CON EXITO')

            return HttpResponseRedirect('/entidades/modi/%s' %
                                        str(form.instance.id))

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

        foto.name = helpers.cambiar_nombre_imagen(
            foto.name, entidad.instance.valor)

        foto = helpers.redimensionar_imagen(entidad.instance.imagen, foto.name)
        # Se envia foto subida y el cambio de nombre, como parametros
        entidad.instance.imagen = foto
        entidad.save()

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

        entidad = Entidad.objects.get(pk=kwargs['pk'])
        form = EntidadForm(
            self.request.POST, self.request.FILES, instance=entidad)

        if form.is_valid():
            if 'imagen' in self.request.FILES:
                self.set_foto(form, (self.request.FILES['imagen']))

            form.save()

            messages.add_message(
                request, messages.SUCCESS, 'ENTIDAD MODIFICADA CON EXITO')

            return HttpResponseRedirect('/entidades/modi/%s' %
                                        str(form.instance.id))

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

        foto.name = helpers.cambiar_nombre_imagen(
            foto.name, entidad.instance.valor)
        foto = helpers.redimensionar_imagen(entidad.instance.imagen, foto.name)
        # Se envia foto subida y el cambio de nombre, como parametros
        entidad.instance.imagen = foto
        entidad.save()

    def get_success_url(self):
        return self.request.get_full_path()


class EntidadDelete(DeleteView):
    model = Entidad

    def get_success_url(self):
        return '/entidades/listado/'