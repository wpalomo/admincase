
import json
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from apps.empleados.models import Empleado
from apps.proveedores.models import Proveedor

from . import helpers
from .forms import (ExpedienteForm, ExpedienteResolucionForm,
                    ExpedienteDisposicionForm, ExpedienteServicioMedicoForm,
                    ExpedienteLicitacionForm, ExpedienteComodatoForm)
from .models import (Expediente, ExpedienteResolucion, ExpedienteDisposicion,
                     ExpedienteServicioMedico, ExpedienteLicitacion, Estado,
                     Etapa, ExpedienteLicitacionCompromiso, ExpedienteComodato,
                     ExpedienteLicitacionOrdenado, FuenteFinanciamiento)


CLASE_EXPEDIENTE = {
    "RESOLUCION": ExpedienteResolucion,
    "DISPOSICION": ExpedienteDisposicion,
    "SERVICIO_MEDICO": ExpedienteServicioMedico,
    "COMODATO": ExpedienteComodato,
    "LICITACION": ExpedienteLicitacion
}


IMPORTE_MEDIO_TRANSACCION_RESOLUCION = 12000


class ExpedienteCreate(CreateView):

    model = Expediente
    form_class = ExpedienteForm

    def post(self, request, *args, **kwargs):

        form = ExpedienteForm(data=self.request.POST)

        if form.is_valid():

            expediente = form.instance
            expediente.etapa = Etapa.objects.get(valor='PREVENTIVO')

            expediente.save()

            messages.add_message(
                request, messages.SUCCESS, 'EXPEDIENTE CREADO CON EXITO')

            return HttpResponseRedirect(
                '/expedientes/modi/' + str(expediente.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expediente_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


class ExpedienteUpdate(UpdateView):

    model = Expediente
    form_class = ExpedienteForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])
        form = ExpedienteForm(instance=expediente)

        tiene_clase_creada = self.tiene_clase_creada(expediente)

        return render_to_response(
            'expedientes/expediente_form.html',
            {
                'form': form,
                'expediente': expediente,
                'tiene_clase_creada': tiene_clase_creada
            },
            context_instance=RequestContext(request)
        )

    def tiene_clase_creada(self, expediente):
        expediente_clase = []
        clase = CLASE_EXPEDIENTE[expediente.clase.valor]

        expediente_clase = clase.objects.filter(expediente=expediente)

        return (len(expediente_clase) > 0)

    def post(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])
        etapa_id = expediente.etapa_id
        etapa = Etapa.objects.get(pk=etapa_id)

        form = ExpedienteForm(self.request.POST, instance=expediente)

        if form.is_valid():

            expediente_update = form.instance
            expediente_update.etapa = etapa

            expediente_update.save()

            messages.add_message(
                request, messages.SUCCESS, 'EXPEDIENTE MODIFICADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expediente_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return self.request.get_full_path()


class ExpedienteListView(ListView):

    model = Expediente
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ExpedienteListView, self).get_context_data(**kwargs)
        context['estados'] = Estado.objects.all()
        context['empleado_solicitante'] = Empleado.objects.all()

        return context

    def get_queryset(self):

        query = super(ExpedienteListView, self).get_queryset()

        parametro1 = self.request.GET.get('parametro1')
        parametro2 = self.request.GET.get('parametro2')

        if self.request.GET.get('filtro') == 'NUMERO_EXPEDIENTE':

            query = self.buscar_por_numero(parametro1, parametro2)

        if self.request.GET.get('filtro') == 'NUMERO_RESOLUCION_PAGO':

            query = self.buscar_por_numero_resolucion_pago(parametro1)

        if self.request.GET.get('filtro') == 'FECHA_EXPEDIENTE':

            query = self.buscar_por_fecha_expediente(
                parametro1, parametro2)

        if self.request.GET.get('filtro') == 'FECHA_RESOLUCION_PAGO':

            query = self.buscar_por_fecha_resolucion_pago(
                parametro1, parametro2)

        if self.request.GET.get('filtro') == 'ESTADO':

            query = self.buscar_por_estado(
                self.request.GET.get('estado'))

        if self.request.GET.get('filtro') == 'SOLICITANTE':

            query = self.buscar_por_empleado_solicitante(
                self.request.GET.get('solicitante'))

        return query

    def buscar_por_numero(self, numero, anio):

        numero = numero.strip()
        anio = anio.strip()

        expedientes = Expediente.objects.filter(
            numero=numero,
            anio__icontains=anio
        )

        return expedientes

    def buscar_por_numero_resolucion_pago(self, numero_resolucion_pago):

        numero_resolucion_pago = numero_resolucion_pago.strip()

        expediente_resolucion_list =\
                ExpedienteResolucion.objects.filter(
                    numero_resolucion_pago=numero_resolucion_pago)\
                    .values('expediente_id')
        expediente_servicio_medico_list =\
            ExpedienteServicioMedico.objects.filter(
                numero_resolucion_pago=numero_resolucion_pago)\
                .values('expediente_id')

        expediente_ids = set(
            [expediente['expediente_id']
             for expediente in expediente_resolucion_list] +
            [expediente['expediente_id']
             for expediente in expediente_servicio_medico_list]
        )

        expedientes = Expediente.objects.filter(pk__in=expediente_ids)
        return expedientes

    def buscar_por_fecha_expediente(self, fecha_desde, fecha_hasta):

        fecha_desde = fecha_desde.strip()
        fecha_hasta = fecha_hasta.strip()

        try:
            fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y')
        except ValueError:
            fecha_desde = datetime.now()

        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y')
        except ValueError:
            fecha_hasta = datetime.now()

        expedientes = Expediente.objects.filter(
            fecha__range=[fecha_desde, fecha_hasta])

        return expedientes

    def buscar_por_fecha_resolucion_pago(self, fecha_desde, fecha_hasta):

        fecha_desde = fecha_desde.strip()
        fecha_hasta = fecha_hasta.strip()

        try:
            fecha_desde = datetime.strptime(fecha_desde, '%d/%m/%Y')
        except ValueError:
            fecha_desde = datetime.now()

        try:
            fecha_hasta = datetime.strptime(fecha_hasta, '%d/%m/%Y')
        except ValueError:
            fecha_hasta = datetime.now()

        expediente_resolucion_list = ExpedienteResolucion.objects.filter(
            fecha_resolucion_pago__range=[fecha_desde, fecha_hasta])\
            .values('expediente_id')
        expediente_servicio_medico_list =\
            ExpedienteServicioMedico.objects.filter(
                fecha_resolucion_pago__range=[fecha_desde, fecha_hasta])\
                .values('expediente_id')

        expediente_ids = set(
            [expediente['expediente_id']
             for expediente in expediente_resolucion_list] +
            [expediente['expediente_id']
             for expediente in expediente_servicio_medico_list]
        )

        expedientes = Expediente.objects.filter(pk__in=expediente_ids)

        return expedientes

    def buscar_por_estado(self, estado):

        expedientes = Expediente.objects.filter(
            estado__descripcion__icontains=estado)

        return expedientes

    def buscar_por_empleado_solicitante(self, empleadoId):

        expedientes = Expediente.objects.filter(
            empleado_solicitante__persona=empleadoId
        )

        # expedientes = Expediente.objects.filter(
        #     Q(empleado_solicitante__persona__apellido__icontains=empleado) |
        #     Q(empleado_solicitante__persona__nombre__icontains=empleado)
        # )

        return expedientes


#-----------------------
# Expediente Resolucion
#-----------------------

class ExpedienteResolucionCreate(CreateView):

    model = ExpedienteResolucion
    form_class = ExpedienteResolucionForm

    def get(self, request, *args, **kwargs):

        form = ExpedienteResolucionForm()

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'expedientes/expedienteresolucion_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = ExpedienteResolucionForm(data=self.request.POST)

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        orden_provision = int(self.request.POST.get("orden_provision"))
        acta_recepcion = int(self.request.POST.get("acta_recepcion"))

        if not helpers.numero_es_valido('ORDEN_PROVISION', orden_provision):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteresolucion_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_provision': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if not helpers.numero_es_valido('ACTA_RECEPCION', acta_recepcion):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteresolucion_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_acta': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if form.is_valid():
            expediente_resolucion = form.save()

            etapa_id = int(self.request.POST.get("etapa"))

            self.actualizar_etapa_estado_expediente(etapa_id, expediente)
            self.guardar_numeros_autoincrementales(expediente_resolucion)

            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')

            return HttpResponseRedirect(
                '/expedientes/resolucion/modi/' +
                str(expediente_resolucion.expediente.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expedienteresolucion_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        expediente.etapa = Etapa.objects.get(pk=etapa_id)

        if expediente.etapa.valor == 'COMPROMISO':
            expediente.estado = Estado.objects.get(valor='PENDIENTE')

        expediente.save()

    def guardar_numeros_autoincrementales(self, expediente_resolucion):
        tipo_transaccion = self.get_tipo_transaccion(
                expediente_resolucion.importe)

        listado = {
            'RESOLUCION_ADJUDICACION':
                expediente_resolucion.resolucion_adjudicacion,
            'ORDEN_PROVISION': expediente_resolucion.orden_provision,
            'ACTA_RECEPCION': expediente_resolucion.acta_recepcion,
            tipo_transaccion:
                expediente_resolucion.numero_identificacion_transaccion
            }

        helpers.registrar_numeros_autoincrementales(listado)

    def get_tipo_transaccion(self, importe):
        if float(importe) > IMPORTE_MEDIO_TRANSACCION_RESOLUCION:
            tipo_transaccion = 'CONTRATACION_DIRECTA'
        else:
            tipo_transaccion = 'COMPRA_DIRECTA'

        return tipo_transaccion


class ExpedienteResolucionUpdate(UpdateView):

    model = ExpedienteResolucion
    form_class = ExpedienteResolucionForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_resolucion = ExpedienteResolucion.objects.get(
            expediente=expediente)

        list_puede_actualizar = self.get_puede_actualizar_numeros(
            expediente_resolucion)

        form = ExpedienteResolucionForm(instance=expediente_resolucion)

        return render_to_response(
            'expedientes/expedienteresolucion_form.html',
            {
                'form': form,
                'expediente': expediente,
                'not_update_numeros_compromiso': list_puede_actualizar[0],
                'not_update_numeros_ordenado': list_puede_actualizar[1]
            },
            context_instance=RequestContext(request)
        )

    def get_puede_actualizar_numeros(self, expediente_resolucion):

        list_puede_actualizar = [False, False]

        if int(expediente_resolucion.orden_provision) > 0 \
               and int(expediente_resolucion.acta_recepcion) > 0:
            list_puede_actualizar[0] = True

        if int(expediente_resolucion.numero_resolucion_pago) > 0:
            list_puede_actualizar[1] = True

        return list_puede_actualizar

    def post(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_resolucion = ExpedienteResolucion.objects.get(
            expediente__id=kwargs['pk'])
        form = ExpedienteResolucionForm(
            self.request.POST, instance=expediente_resolucion)

        orden_provision = int(self.request.POST.get("orden_provision"))
        acta_recepcion = int(self.request.POST.get("acta_recepcion"))
        resolucion_pago = int(self.request.POST.get("numero_resolucion_pago"))

        if not helpers.numero_es_valido('ORDEN_PROVISION', orden_provision):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteresolucion_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_provision': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if not helpers.numero_es_valido('ACTA_RECEPCION', acta_recepcion):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteresolucion_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_acta': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if resolucion_pago > 0:
            if not helpers.numero_es_valido('RESOLUCION_PAGO', resolucion_pago):
                messages.add_message(
                    request, messages.ERROR, 'EL FORMULARIO TIENE ERRORES')

                return render_to_response(
                    'expedientes/expedienteresolucion_form.html',
                    {
                        'form': form,
                        'expediente': expediente,
                        'error_resolucion_pago': 'Numero no valido'
                    },
                    context_instance=RequestContext(request)
                )

        if form.is_valid():
            form.save()

            etapa_id = int(self.request.POST.get("etapa"))

            self.actualizar_etapa_estado_expediente(etapa_id, expediente)

            listado = {
                'ORDEN_PROVISION': orden_provision,
                'ACTA_RECEPCION': acta_recepcion,
                'RESOLUCION_PAGO': resolucion_pago,
                }

            helpers.registrar_numeros_autoincrementales(listado)

            messages.add_message(
                request, messages.SUCCESS, 'SE HA ACTUALIZADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expedienteresolucion_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        expediente.etapa = Etapa.objects.get(pk=etapa_id)

        if expediente.etapa.valor == 'COMPROMISO':
            expediente.estado = Estado.objects.get(valor='PENDIENTE')

        elif expediente.etapa.valor == 'ORDENADO':
            expediente.estado = Estado.objects.get(valor='CERRADO')

        expediente.save()

    def get_success_url(self):
        return self.request.get_full_path()


#-----------------------
# Expediente Disposicion
#-----------------------

class ExpedienteDisposicionCreate(CreateView):
    model = ExpedienteDisposicion
    form_class = ExpedienteDisposicionForm

    def get(self, request, *args, **kwargs):

        form = ExpedienteDisposicionForm()

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'expedientes/expedientedisposicion_form.html',
            {
                'form': form,
                'expediente': expediente
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = ExpedienteDisposicionForm(data=self.request.POST)

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        if form.is_valid():
            expediente_disposicion = form.save()

            etapa_id = int(self.request.POST['etapa'])

            self.actualizar_etapa_estado_expediente(etapa_id, expediente)
            self.guardar_numeros_autoincrementales(expediente_disposicion)

            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')

            return HttpResponseRedirect(
                '/expedientes/disposicion/modi/'
                + str(expediente_disposicion.expediente.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expedientedisposicion_form.html',
            {
                'form': form,
                'expediente': expediente
            },
            context_instance=RequestContext(request)
        )

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        etapa = Etapa.objects.get(pk=etapa_id)
        expediente.etapa = etapa

        if expediente.etapa.valor == "COMPROMISO_ORDENADO":
            expediente.estado = Estado.objects.get(valor="CERRADO")

        expediente.save()

    def guardar_numeros_autoincrementales(self, expediente_disposicion):

        listado = {
            'CONTRATACION_DIRECTA':
                expediente_disposicion.contratacion_directa,
            'NUMERO_DISPOSICION': expediente_disposicion.numero_disposicion
        }

        helpers.registrar_numeros_autoincrementales(listado)


class ExpedienteDisposicionUpdate(UpdateView):
    model = ExpedienteDisposicion
    form_class = ExpedienteDisposicionForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_disposicion = ExpedienteDisposicion.objects.get(
            expediente=expediente)

        form = ExpedienteDisposicionForm(instance=expediente_disposicion)

        return render_to_response(
            'expedientes/expedientedisposicion_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )


#---------------------------
# Expediente Servicio Medico
#---------------------------

class ExpedienteServicioMedicoCreate(CreateView):

    model = ExpedienteServicioMedico
    form_class = ExpedienteServicioMedicoForm

    def get(self, request, *args, **kwargs):

        form = ExpedienteServicioMedicoForm()

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'expedientes/expedienteserviciomedico_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = ExpedienteServicioMedicoForm(data=self.request.POST)

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        orden_provision = int(self.request.POST.get("orden_provision"))
        acta_recepcion = int(self.request.POST.get("acta_recepcion"))
        resolucion_pago = int(self.request.POST.get("numero_resolucion_pago"))

        if not helpers.numero_es_valido('ORDEN_PROVISION', orden_provision):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteserviciomedico_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_provision': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if not helpers.numero_es_valido('ACTA_RECEPCION', acta_recepcion):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteserviciomedico_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_acta': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if not helpers.numero_es_valido('RESOLUCION_PAGO', resolucion_pago):
            messages.add_message(
                request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

            return render_to_response(
                'expedientes/expedienteserviciomedico_form.html',
                {
                    'form': form,
                    'expediente': expediente,
                    'error_resolucion_pago': 'Numero no valido'
                },
                context_instance=RequestContext(request)
            )

        if form.is_valid():
            expediente_servicio_medico = form.save()

            etapa_id = int(self.request.POST.get("etapa"))

            self.actualizar_etapa_estado_expediente(etapa_id, expediente)

            listado = {
                'ORDEN_PROVISION': expediente_servicio_medico.orden_provision,
                'ACTA_RECEPCION': expediente_servicio_medico.acta_recepcion,
                'RESOLUCION_PAGO':
                    expediente_servicio_medico.numero_resolucion_pago
                }

            helpers.registrar_numeros_autoincrementales(listado)

            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')

            return HttpResponseRedirect(
                '/expedientes/serviciomedico/modi/' +
                str(expediente_servicio_medico.expediente.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expedienteserviciomedico_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        etapa = Etapa.objects.get(pk=etapa_id)
        expediente.etapa = etapa

        if expediente.etapa.valor == "COMPROMISO_ORDENADO":
            expediente.estado = Estado.objects.get(valor="CERRADO")

        expediente.save()


class ExpedienteServicioMedicoUpdate(UpdateView):

    model = ExpedienteServicioMedico
    form_class = ExpedienteServicioMedicoForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_servicio_medico = ExpedienteServicioMedico.objects.get(
            expediente=expediente)

        form = ExpedienteServicioMedicoForm(instance=expediente_servicio_medico)

        return render_to_response(
            'expedientes/expedienteserviciomedico_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )


#-----------------------
# Expediente Licitación
#-----------------------

class ExpedienteLicitacionCreate(CreateView):

    model = ExpedienteLicitacion
    form_class = ExpedienteLicitacionForm

    def get(self, request, *args, **kwargs):

        form = ExpedienteLicitacionForm()
        expediente = Expediente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'expedientes/expedientelicitacion_form.html',
            {
                'form': form,
                'expediente': expediente
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = ExpedienteLicitacionForm(data=self.request.POST)

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        if form.is_valid():
            expediente_licitacion = form.save()

            etapa_id = int(self.request.POST.get("etapa"))

            datos = json.loads(self.request.POST['items_proveedor'])

            self.guardar_items_compromiso(datos, expediente_licitacion)
            self.actualizar_etapa_estado_expediente(etapa_id, expediente)

            messages.add_message(
                request, messages.SUCCESS, 'SE HA CREADO CON EXITO')

            return HttpResponseRedirect(
                '/expedientes/licitacion/modi/' +
                str(expediente_licitacion.expediente.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expedientelicitacion_form.html',
            {
                'form': form,
                'expediente': expediente
            },
            context_instance=RequestContext(request)
        )

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        expediente.etapa = Etapa.objects.get(pk=etapa_id)

        if expediente.etapa.valor == 'COMPROMISO':
            expediente.estado = Estado.objects.get(valor='PENDIENTE')

        expediente.save()

    def guardar_numeros_autoincrementales(self, licitacion_compromiso):
        listado = {
            'RESOLUCION_ADJUDICACION':
            licitacion_compromiso.expediente_licitacion.resolucion_adjudicacion,
            'ORDEN_PROVISION': licitacion_compromiso.orden_provision,
            'ACTA_RECEPCION': licitacion_compromiso.acta_recepcion,
            'NUMERO_DISPOSICION':
                licitacion_compromiso.expediente_licitacion.numero_disposicion,
            'NUMERO_LICITACION':
                licitacion_compromiso.expediente_licitacion.numero,
        }

        helpers.registrar_numeros_autoincrementales(listado)

    def guardar_items_compromiso(self, datos, expediente_licitacion):

        for item in datos:
            proveedor = Proveedor.objects.get(razon_social=item['proveedor'])

            if item["orden_provision"]:
                orden_provision = int(item["orden_provision"])
            else:
                orden_provision = \
                    helpers.get_numero_autoincremental('ORDEN_PROVISION')

            acta_recepcion = \
                helpers.get_numero_autoincremental('ACTA_RECEPCION')

            expediente_licitacion_compromiso =\
                ExpedienteLicitacionCompromiso.objects.create(
                    expediente_licitacion=expediente_licitacion,
                    proveedor=proveedor,
                    monto=item['monto'],
                    monto_total=item['monto_total'],
                    orden_provision=orden_provision,
                    acta_recepcion=acta_recepcion
                )

            self.guardar_numeros_autoincrementales(
                expediente_licitacion_compromiso)


class ExpedienteLicitacionUpdate(UpdateView):

    model = ExpedienteLicitacion
    form_class = ExpedienteLicitacionForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_licitacion = ExpedienteLicitacion.objects.get(
            expediente=expediente)

        expediente_licitacion_compromiso = \
            expediente_licitacion.expedientelicitacioncompromiso_set.all()

        expediente_licitacion_ordenado = \
            expediente_licitacion.expedientelicitacionordenado_set.all()

        form = ExpedienteLicitacionForm(instance=expediente_licitacion)

        return render_to_response(
            'expedientes/expedientelicitacion_form.html',
            {
                'form': form,
                'expediente': expediente,
                'expediente_licitacion_compromiso_list':
                    expediente_licitacion_compromiso,
                'expediente_licitacion_ordenado_list':
                    expediente_licitacion_ordenado
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        etapa_id = int(self.request.POST.get("etapa"))

        datos = json.loads(self.request.POST['items_ordenado'])

        expediente_licitacion = ExpedienteLicitacion.objects.get(
            expediente=expediente)

        self.guardar_items_ordenado(datos, expediente_licitacion)
        self.actualizar_etapa_estado_expediente(etapa_id, expediente)

        messages.add_message(
            request, messages.SUCCESS, 'SE HA ACTUALIZADO CON EXITO')

        return HttpResponseRedirect(self.get_success_url())

    def guardar_numeros_autoincrementales(self, licitacion_ordenado):

        listado = {
            'RESOLUCION_PAGO': licitacion_ordenado.numero_resolucion_pago
        }

        helpers.registrar_numeros_autoincrementales(listado)

    def actualizar_etapa_estado_expediente(self, etapa_id, expediente):

        expediente.etapa = Etapa.objects.get(pk=etapa_id)

        if expediente.etapa.valor == 'ORDENADO':
            expediente.estado = Estado.objects.get(valor='CERRADO')

        expediente.save()

    def guardar_items_ordenado(self, datos, expediente_licitacion):

        for item in datos:
            proveedor = Proveedor.objects.get(razon_social=item['proveedor'])

            if item["resolucion_pago"]:
                resolucion_pago = int(item["resolucion_pago"])
            else:
                resolucion_pago = \
                    helpers.get_numero_autoincremental('RESOLUCION_PAGO')

            solicitante_resolucion_pago = Empleado.objects.get(
                pk=int(item['solicitante']))

            try:
                fecha_resolucion_pago = datetime.strptime(
                    item["fecha_resolucion_pago"], '%d/%m/%Y')
            except ValueError:
                messages.add_message(
                    self.request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

                return render_to_response(
                    'expedientes/expedientelicitacion_form.html',
                    {
                        'form': self.form,
                        'expediente': self.expediente
                    },
                    context_instance=RequestContext(self.request)
                )

            expediente_licitacion_ordenado = \
                ExpedienteLicitacionOrdenado.objects.create(
                    expediente_licitacion=expediente_licitacion,
                    proveedor=proveedor,
                    monto=item["monto"],
                    monto_total=item["monto_total"],
                    orden_provision=int(item["orden_provision"]),
                    acta_recepcion=int(item["acta_recepcion"]),
                    numero_resolucion_pago=resolucion_pago,
                    fecha_resolucion_pago=fecha_resolucion_pago,
                    solicitante_resolucion_pago=solicitante_resolucion_pago,
                    observaciones=item["observaciones"]
                )

            self.guardar_numeros_autoincrementales(
                expediente_licitacion_ordenado)

    def get_success_url(self):
        return self.request.get_full_path()


#-----------------------
# Expediente Comodato
#-----------------------

class ExpedienteComodatoUpdate(UpdateView):
    model = ExpedienteComodato
    form_class = ExpedienteComodatoForm

    def get(self, request, *args, **kwargs):

        expediente = Expediente.objects.get(pk=kwargs['pk'])

        expediente_comodato = ExpedienteComodato.objects.filter(
            expediente=expediente)

        #form = ExpedienteComodatoForm(instance=expediente_comodato)

        return render_to_response(
            'expedientes/expedientecomodato_modi.html',
            {
                #'form': form,
                'expediente': expediente,
                'expediente_comodato': expediente_comodato
            },
            context_instance=RequestContext(request)
        )


class ExpedienteComodatoCreate(CreateView):
    model = ExpedienteComodato
    form_class = ExpedienteComodatoForm

    def get(self, request, *args, **kwargs):

        form = ExpedienteComodatoForm()
        expediente = Expediente.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'expedientes/expedientecomodato_form.html',
            {'form': form, 'expediente': expediente},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        id_expediente = int(self.request.POST['expediente'])
        datos = json.loads(self.request.POST['comodato'])
        expediente = Expediente.objects.get(id=id_expediente)

        try:
            comodato = ExpedienteComodato.objects.latest('id')
            resolucion = comodato.resolucion_pago
            orden = comodato.orden_provision
            contratacion = comodato.numero_contratacion_directa
        except:
            resolucion = 0
            orden = 0
            contratacion = 0

        for item in datos:
            if item['resolucion_pago'] == '':
                resolucion_pago = helpers.get_numero_autoincremental('RESOLUCION_PAGO')
                helpers.guardar_numero_autoincremental('RESOLUCION_PAGO', resolucion_pago)
            else:
                resolucion_pago = item['resolucion_pago']

            if item['orden_provision'] == '':
                orden_provision = helpers.get_numero_autoincremental('ORDEN_PROVISION')
                helpers.guardar_numero_autoincremental('ORDEN_PROVISION', orden_provision)
            else:
                orden_provision = item['orden_provision']

            numero_contratacion_directa = helpers.get_numero_autoincremental('CONTRATACION_DIRECTA')
            helpers.guardar_numero_autoincremental('CONTRATACION_DIRECTA', numero_contratacion_directa)

            ExpedienteComodato.objects.create(
                expediente=expediente,
                proveedor=Proveedor.objects.get(id=item['proveedor']),
                resolucion_contratacion=item['resolucion_contratacion'],
                fecha_resolucion_contratacion=item['fecha_resolucion_contratacion'],
                numero_contratacion_directa=numero_contratacion_directa,
                importe=item['importe'],
                orden_provision=orden_provision,
                resolucion_pago=resolucion_pago,
                fecha_resolucion_pago=item['fecha_resolucion_pago'],
                solicitante_resolucion_pago=Empleado.objects.get(pk=int(item['solicitante_resolucion_pago'])),
                fuente_financiamiento=FuenteFinanciamiento.objects.get(pk=int(item['fuente_financiamiento'])),
                observaciones=item['observaciones'])


        expediente.estado = Estado.objects.get(valor='CERRADO')
        expediente.etapa = Etapa.objects.get(valor='COMPROMISO_ORDENADO')
        expediente.save()
        expediente_comodato = ExpedienteComodato.objects.filter(expediente=expediente)

        return render_to_response('expedientes/expedientecomodato_modi.html',
                                  {
                                      'expediente':expediente,
                                      'expediente_comodato': expediente_comodato
                                  })
