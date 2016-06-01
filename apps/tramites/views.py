
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.clientes.models import Cliente
from apps.complementos.organigrama.models import Entidad
from apps.tramites.models import (Tramite, TipoTramite, RequisitoTramite,
                                  Requisito, RequisitoTipoTramite)

from .forms import TramiteForm, TipoTramiteForm


class TramiteListView(ListView):
    model = Tramite
    paginate_by = 10

    def get_queryset(self):

        query = super(TramiteListView, self).get_queryset()

        return query


class TramiteCreate(CreateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):
        form = TramiteForm()

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = TramiteForm(data=self.request.POST)

        cliente = Cliente.objects.get(pk=int(self.request.POST['cliente']))

        if form.is_valid():
            tramite = form.save()

            requisitos_tramite = self.request.POST['requisitos_presentados']

            if requisitos_tramite:
                parametros = requisitos_tramite.split("|")

                for item in parametros:
                    print(item)
                    requisito_parametro = item.split("#")

                    requisito = Requisito.objects.get(
                        valor=requisito_parametro[0])

                    presentado = (False, True)[requisito_parametro[1] == '1']

                    RequisitoTramite.objects.create(
                        tramite=tramite,
                        requisito=requisito,
                        presentado=presentado
                    )

            messages.add_message(
                request, messages.SUCCESS, 'EL TRAMITE SE HA CREADO CON EXITO')

            return HttpResponseRedirect('/tramites/modi/' + str(tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente
            },
            context_instance=RequestContext(request)
        )


class TramiteUpdate(UpdateView):
    model = Tramite
    form_class = TramiteForm

    def get(self, request, *args, **kwargs):
        tramite = Tramite.objects.get(pk=kwargs['pk'])
        cliente = Cliente.objects.get(pk=tramite.cliente.id)
        requisitos_tramite = tramite.requisitotramite_set.all()

        form = TramiteForm(instance=tramite)

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'cliente': cliente,
                'requisitos': requisitos_tramite
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        tramite = Tramite.objects.get(pk=kwargs['pk'])

        cliente = Cliente.objects.get(pk=tramite.cliente.id)

        requisitos_tramite = tramite.requisitotramite_set.all()

        form = TramiteForm(self.request.POST, instance=tramite)

        if form.is_valid():
            form.save()

            requisitos = self.request.POST['requisitos_presentados']

            if requisitos:
                parametros = requisitos.split("|")

                # print(requisitos)

                for item in parametros:
                    requisito_parametro = item.split("#")
                    requisito = RequisitoTramite.objects.get(
                        requisito__valor=requisito_parametro[0])
                    presentado = (False, True)[requisito_parametro[1] == '1']
                    requisito.presentado = presentado
                    requisito.save()

            messages.add_message(
                request, messages.SUCCESS,
                'EL TRAMITE SE HA ACTUALIZADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tramite_form.html',
            {
                'form': form,
                'tramite': tramite,
                'cliente': cliente,
                'requisitos': requisitos_tramite
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class TramiteDelete(DeleteView):

    model = Tramite
    success_message = 'El trámite fue eliminado con éxito'

    def get_success_url(self):
        tramite = Tramite.objects.get(pk=self.kwargs['pk'])
        cliente = Cliente.objects.get(pk=tramite.cliente.id)

        return '/tramites/listado/' + str(cliente.id)


class TramiteClienteListView(ListView):
    model = Tramite
    paginate_by = 10

    def get(self, request, *args, **kwargs):

        cliente = Cliente.objects.get(pk=kwargs['pk'])

        tramite_cliente = Tramite.objects.filter(cliente__id=cliente.id)

        return render_to_response(
            'tramites/tramite_cliente_list.html',
            {
                'cliente': cliente,
                'tramite_cliente': tramite_cliente
            },
            context_instance=RequestContext(request)
        )


class TipoTramiteListView(ListView):
    model = TipoTramite
    paginate_by = 10

    def get_queryset(self):

        query = super(TipoTramiteListView, self).get_queryset()

        return query


class TipoTramiteCreate(CreateView):
    model = TipoTramite
    form_class = TipoTramiteForm

    def get(self, request, *args, **kwargs):

        form = TipoTramiteForm()

        requisitos = Requisito.objects.all()

        return render_to_response(
            'tramites/tipotramite_form.html',
            {
                'form': form,
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = TipoTramiteForm(data=self.request.POST)

        requisitos = Requisito.objects.all()

        if form.is_valid():
            tipo_tramite = form.save()

            requisitos_tramite = self.request.POST['requisitos_presentados']

            if requisitos_tramite:
                parametros = requisitos_tramite.split("|")

                for item in parametros:
                    requisito_necesario = item.split("#")

                    requisito = Requisito.objects.get(
                        valor=requisito_necesario[0])

                    es_requisito = (False, True)[requisito_necesario[1] == '1']

                    # if es_requisito:
                    RequisitoTipoTramite.objects.create(
                        tipo_tramite=tipo_tramite,
                        requisito=requisito,
                        estado=es_requisito
                    )

            messages.add_message(
                request, messages.SUCCESS,
                'EL TIPO DE TRAMITE SE HA CREADO CON EXITO')

            return HttpResponseRedirect('/tramites/tipo/modi/' +
                                        str(tipo_tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tipotramite_form.html',
            {
                'form': form,
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )


class TipoTramiteUpdate(UpdateView):
    model = TipoTramite
    form_class = TipoTramiteForm

    def get(self, request, *args, **kwargs):

        tipo_tramite = TipoTramite.objects.get(pk=kwargs['pk'])
        form = TipoTramiteForm(instance=tipo_tramite)

        requisitos = tipo_tramite.requisitotipotramite_set.all()

        return render_to_response(
            'tramites/tipotramite_form.html',
            {
                'form': form,
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        tipo_tramite = TipoTramite.objects.get(pk=kwargs['pk'])
        form = TipoTramiteForm(data=self.request.POST, instance=tipo_tramite)

        requisitos = tipo_tramite.requisitotipotramite_set.all()

        if form.is_valid():
            tipo_tramite = form.save()

            requisitos_tramite = self.request.POST['requisitos_presentados']

            if requisitos_tramite:
                parametros = requisitos_tramite.split("|")

                for item in parametros:
                    requisito_necesario = item.split("#")
                    requisito_tramite = RequisitoTipoTramite.objects.get(
                        tipo_tramite__id=tipo_tramite.id,
                        requisito__valor=requisito_necesario[0])
                    es_necesario = (False, True)[requisito_necesario[1] == '1']
                    requisito_tramite.estado = es_necesario
                    requisito_tramite.save()


            messages.add_message(
                request, messages.SUCCESS,
                'EL TIPO DE TRAMITE SE HA MODIFICADO  CON EXITO')

            return HttpResponseRedirect('/tramites/tipo/modi/' +
                                        str(tipo_tramite.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'tramites/tipotramite_form.html',
            {
                'form': form,
                'requisitos': requisitos
            },
            context_instance=RequestContext(request)
        )


class TipoTramiteDelete(DeleteView):
    model = TipoTramite