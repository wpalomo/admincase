
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from apps.empleados.models import Empleado
from apps.complementos.salud.models import Especialidad

from . import helpers
from .forms import (AgendaForm, AgendaDiaConfiguracionForm,
                    AgendaFechaDetalleForm, AgendaBloqueoForm, 
                    AgendaDiaConfiguracionBloqueoForm)
from .models import (Agenda, AgendaDiaConfiguracion, AgendaFechaDetalle,
                     TipoAgenda, AgendaFechaDetalleBloqueo, MotivoBloqueo,
                     AgendaDiaConfiguracionBloqueo, AgendaPeriodoBloqueo)


class AgendaCreate(CreateView):

    model = Agenda
    form_class = AgendaForm

    def post(self, request, *args, **kwargs):

        form = AgendaForm(data=self.request.POST)

        if form.is_valid():

            agenda = form.save()

            messages.add_message(
                request, messages.SUCCESS, 'AGENDA CREADA CON EXITO')

            return HttpResponseRedirect('/agendas/modi/' + str(agenda.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'agendas/agenda_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )


class AgendaUpdate(UpdateView):

    model = Agenda
    form_class = AgendaForm

    def get(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        form = AgendaForm(instance=agenda)

        agenda_dia_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda)

        not_update = False

        if agenda_dia_configuracion:
            messages.add_message(
                request,
                messages.INFO,
                'SI DESEA MODIFICAR LA AGENDA, PRIMERO DEBE ELIMINAR LAS '
                'CONFIGURACIONES GENERICAS POR DIA.'
                )

            not_update = True

        return render_to_response(
            'agendas/agenda_form.html',
            {'form': form, 'agenda': agenda, 'not_update': not_update},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        form = AgendaForm(self.request.POST, instance=agenda)

        if form.is_valid():

            agenda = form.save()

            messages.add_message(
                request, messages.SUCCESS, 'AGENDA MODIFICADA CON EXITO')

            return HttpResponseRedirect('/agendas/modi/' + str(agenda.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'agendas/agenda_form.html',
            {'form': form, 'agenda': agenda},
            context_instance=RequestContext(request)
        )


class AgendaListView(ListView):

    model = Agenda
    paginate_by = 10

    def get_queryset(self):

        query = super(AgendaListView, self).get_queryset()

        if self.request.GET.get('filtro') == 'TODOS':

            query = Agenda.objects.all()

        elif self.request.GET.get('filtro') == 'PROFESIONAL':

            profesional = self.request.GET.get('profesional')
            query = self.buscar_por_profesional(profesional)

        elif self.request.GET.get('filtro') == 'ESPECIALIDAD':

            especialidad = self.request.GET.get('especialidad')
            query = self.buscar_por_especialidad(especialidad)

        elif self.request.GET.get('filtro') == 'TIPO_AGENDA':

            tipo_agenda = self.request.GET.get('tipo_agenda')
            query = self.buscar_por_tipo_agenda(tipo_agenda)

        return query

    def buscar_por_profesional(self, profesional):

        try:
            empleado = Empleado.objects.get(pk=profesional)
        except:
            empleado = None

        agendas = Agenda.objects.filter(profesional=empleado)

        return agendas

    def buscar_por_especialidad(self, especialidad):

        try:
            especialidad = Especialidad.objects.get(pk=especialidad)
        except:
            especialidad = None

        agendas = Agenda.objects.filter(especialidad=especialidad)

        return agendas

    def buscar_por_tipo_agenda(self, tipo_agenda):

        try:
            tipo = TipoAgenda.objects.get(pk=tipo_agenda)
        except:
            tipo = None

        agendas = Agenda.objects.filter(tipo_agenda=tipo)

        return agendas


# ----------------------------
# AGENDA DIAS CONFIGURACION
# ----------------------------

class AgendaDiaConfiguracionCreate(CreateView):

    model = AgendaDiaConfiguracion
    form_class = AgendaDiaConfiguracionForm

    def get(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        agenda_dia_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda)
        form = AgendaDiaConfiguracionForm(especialidad=agenda.especialidad.id)

        return render_to_response(
            'agendas/agenda_dia_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': agenda_dia_configuracion
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        form = AgendaDiaConfiguracionForm(
            especialidad=agenda.especialidad.id, data=self.request.POST)

        if form.is_valid():

            dia_configuracion = form.save()

            self.generar_fechas_agenda(dia_configuracion)

            messages.add_message(
                request, messages.SUCCESS, 'CONFIGURACION AGREGADA CON EXITO')

            return HttpResponseRedirect(
                '/agendas/configuracion_por_dias/' + str(agenda.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        agenda_dia_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda)

        return render_to_response(
            'agendas/agenda_dia_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': agenda_dia_configuracion
            },
            context_instance=RequestContext(request)
        )

    def generar_fechas_agenda(self, dia_configuracion):

        fecha_desde = datetime.datetime.strptime(
            str(dia_configuracion.fecha_desde), '%Y-%m-%d')

        if (dia_configuracion.dia.numero == fecha_desde.weekday()):
            self.guardar_fecha_detalle(fecha_desde, dia_configuracion)

        cantidad_dias = helpers.get_cantidad_dias_entre_fechas(
            dia_configuracion.fecha_desde, dia_configuracion.fecha_hasta)

        cantidad_dias += 1  # se suma 1 para que abarque hasta fecha_hasta

        for dia_siguiente in range(1, cantidad_dias):
            fecha = fecha_desde + datetime.timedelta(days=dia_siguiente)
            if (dia_configuracion.dia.numero == fecha.weekday()):
                self.guardar_fecha_detalle(fecha, dia_configuracion)

    def guardar_fecha_detalle(self, fecha, dia_configuracion):

        AgendaFechaDetalle.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha=fecha,
            hora_desde=dia_configuracion.hora_desde,
            hora_hasta=dia_configuracion.hora_hasta,
            duracion_minutos=dia_configuracion.duracion_minutos,
            practica=dia_configuracion.practica
            )


class AgendaDiaConfiguracionUpdate(UpdateView):

    model = AgendaDiaConfiguracion
    form_class = AgendaDiaConfiguracionForm

    def get(self, request, *args, **kwargs):

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=kwargs['pk'])
        agenda = Agenda.objects.get(pk=dia_configuracion.agenda.id)
        agenda_dia_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda)

        form = AgendaDiaConfiguracionForm(
            especialidad=agenda.especialidad.id, instance=dia_configuracion)

        messages.add_message(
            request,
            messages.SUCCESS,
            'ATENCION!! LA MODIFICACION DE ESTA CONFIGURACION PROVOCARA UN '
            'SETEO MASIVO EN LA CONFIGURACION POR FECHAS.'
            )

        return render_to_response(
            'agendas/agenda_dia_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': agenda_dia_configuracion
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=kwargs['pk'])
        agenda = Agenda.objects.get(pk=dia_configuracion.agenda.id)
        agenda_dia_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda)

        form = AgendaDiaConfiguracionForm(
            agenda.especialidad.id,
            self.request.POST,
            instance=dia_configuracion
            )

        if form.is_valid():

            dia_configuracion = form.save()

            self.generar_fechas_agenda(dia_configuracion)

            messages.add_message(
                request, messages.SUCCESS, 'MODIFICACION EXITOSA!')

            return HttpResponseRedirect(
                '/agendas/configuracion_por_dias/' + str(agenda.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'agendas/agenda_dia_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': agenda_dia_configuracion
            },
            context_instance=RequestContext(request)
        )

    def generar_fechas_agenda(self, dia_configuracion):

        AgendaFechaDetalle.objects.filter(
            dia_configuracion=dia_configuracion).delete()

        fecha_desde = datetime.datetime.strptime(
            str(dia_configuracion.fecha_desde), '%Y-%m-%d')

        if (dia_configuracion.dia.numero == fecha_desde.weekday()):
            self.guardar_fecha_detalle(fecha_desde, dia_configuracion)

        cantidad_dias = helpers.get_cantidad_dias_entre_fechas(
            dia_configuracion.fecha_desde, dia_configuracion.fecha_hasta)

        cantidad_dias += 1  # se suma 1 para que abarque hasta fecha_hasta

        for dia_siguiente in range(1, cantidad_dias):
            fecha = fecha_desde + datetime.timedelta(days=dia_siguiente)
            if (dia_configuracion.dia.numero == fecha.weekday()):
                self.guardar_fecha_detalle(fecha, dia_configuracion)

    def guardar_fecha_detalle(self, fecha, dia_configuracion):
        agenda_fecha_detalle = AgendaFechaDetalle.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha=fecha,
            hora_desde=dia_configuracion.hora_desde,
            hora_hasta=dia_configuracion.hora_hasta,
            duracion_minutos=dia_configuracion.duracion_minutos,
            practica=dia_configuracion.practica
            )

        return agenda_fecha_detalle


class AgendaDiaConfiguracionDelete(DeleteView):

    model = AgendaDiaConfiguracion
    template_name = 'agendas/agenda_dia_configuracion_delete.html'

    def dispatch(self, *args, **kwargs):
        configuracion = AgendaDiaConfiguracion.objects.get(id=kwargs['pk'])
        self.agenda_id = configuracion.agenda.id
        return super(AgendaDiaConfiguracionDelete, self).dispatch(
            *args, **kwargs)

    def post(self, request, *args, **kwargs):

        AgendaFechaDetalle.objects.filter(
            dia_configuracion__id=kwargs['pk']).delete()

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=kwargs['pk'])
        agenda_id = dia_configuracion.agenda.id
        dia_configuracion.delete()

        return HttpResponseRedirect(
                '/agendas/configuracion_por_dias/' + str(agenda_id))

    def get_success_url(self):
        return '/agendas/configuracion_por_dias/' + str(self.agenda_id)


# ----------------------------
# AGENDA FECHAS CONFIGURACION
# ----------------------------


class AgendaFechaDetalleCreate(DeleteView):

    model = AgendaFechaDetalleForm
    template_name = 'agendas/agenda_fecha_configuracion_form.html'

    def dispatch(self, *args, **kwargs):
        self.configuracion = AgendaDiaConfiguracion.objects.get(id=kwargs['pk'])
        return super(AgendaFechaDetalleCreate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=self.configuracion.agenda.id)
        listado_fechas_configuracion = AgendaFechaDetalle.objects.filter(
            dia_configuracion=self.configuracion)

        form = AgendaFechaDetalleForm(especialidad=agenda.especialidad.id)

        return render_to_response(
            'agendas/agenda_fecha_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': self.configuracion,
                'agenda_fechas_configuracion': listado_fechas_configuracion
            },
            context_instance=RequestContext(request)
        )


class AgendaFechaDetalleUpdate(DeleteView):

    model = AgendaFechaDetalleForm
    template_name = 'agendas/agenda_fecha_configuracion_form.html'

    def dispatch(self, *args, **kwargs):
        self.fecha_configuracion = AgendaFechaDetalle.objects.get(
            id=kwargs['pk'])
        self.dia_config_id = self.fecha_configuracion.dia_configuracion.id
        return super(AgendaFechaDetalleUpdate, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=self.fecha_configuracion.dia_configuracion.id)

        listado_fechas_configuracion = AgendaFechaDetalle.objects.filter(
            dia_configuracion=dia_configuracion)

        agenda = Agenda.objects.get(pk=self.fecha_configuracion.agenda.id)

        form = AgendaFechaDetalleForm(
            especialidad=agenda.especialidad.id,
            instance=self.fecha_configuracion
            )

        return render_to_response(
            'agendas/agenda_fecha_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': dia_configuracion,
                'agenda_fechas_configuracion': listado_fechas_configuracion,
                'fecha_configuracion': self.fecha_configuracion
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=self.fecha_configuracion.agenda.id)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=self.fecha_configuracion.dia_configuracion.id)

        listado_fechas_configuracion = AgendaFechaDetalle.objects.filter(
            dia_configuracion=dia_configuracion)

        form = AgendaFechaDetalleForm(
            agenda.especialidad.id,
            self.request.POST,
            instance=self.fecha_configuracion
            )

        if form.is_valid():

            form.save()

            messages.add_message(
                request, messages.SUCCESS, 'MODIFICACION EXITOSA!')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'agendas/agenda_fecha_configuracion_form.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': dia_configuracion,
                'agenda_fechas_configuracion': listado_fechas_configuracion,
                'fecha_configuracion': self.fecha_configuracion
            },
            context_instance=RequestContext(request)
        )

    def get_success_url(self):
        return '/agendas/configuracion_por_fechas/' + str(self.dia_config_id)


# ----------------------------
# BLOQUEOS DE AGENDA
# ----------------------------

class AgendaBloqueoCreate(CreateView):

    form_class = AgendaBloqueoForm

    def get(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        bloqueos_por_fechas = AgendaFechaDetalleBloqueo.objects.filter(
            agenda=agenda)
        dia_configuracion = AgendaDiaConfiguracion.objects.filter(agenda=agenda)
        dia_configuracion_bloqueo = \
            AgendaDiaConfiguracionBloqueo.objects.filter(agenda=agenda)
        periodos_bloqueo = AgendaPeriodoBloqueo.objects.filter(agenda=agenda)

        form = AgendaBloqueoForm(agenda=agenda.id)

        return render_to_response(
            'agendas/agenda_bloqueos.html',
            {
                'form': form,
                'agenda': agenda,
                'agenda_dia_configuracion': dia_configuracion,
                'bloqueos_por_fechas': bloqueos_por_fechas,
                'bloqueos_por_dia_configuracion': dia_configuracion_bloqueo,
                'bloqueos_por_periodos': periodos_bloqueo
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        bloqueo_por_fecha = self.request.POST.get('BLOQUEO_POR_FECHA', None)
        bloqueo_por_periodo = self.request.POST.get('BLOQUEO_POR_PERIODO', None)

        if bloqueo_por_fecha:

            fecha_id = self.request.POST['bloqueo_por_fecha_fecha']
            motivo_bloqueo_id = \
                self.request.POST['bloqueo_por_fecha_motivo_bloqueo']
            observaciones = self.request.POST['bloqueo_por_fecha_observaciones']

            if not fecha_id or not motivo_bloqueo_id:

                messages.add_message(
                    request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

                return HttpResponseRedirect(
                    '/agendas/bloqueo/' + str(agenda.id))

            fecha_detalle = AgendaFechaDetalle.objects.get(pk=fecha_id)
            motivo_bloqueo = MotivoBloqueo.objects.get(pk=motivo_bloqueo_id)

            AgendaFechaDetalleBloqueo.objects.create(
                agenda=agenda,
                dia_configuracion=fecha_detalle.dia_configuracion,
                fecha_detalle=fecha_detalle,
                motivo_bloqueo=motivo_bloqueo,
                observacion=observaciones
                )

            messages.add_message(
                request, messages.ERROR, 'BLOQUEO AGREGADO')

            return HttpResponseRedirect(
                '/agendas/bloqueo/' + str(agenda.id))

        elif bloqueo_por_periodo:

            fecha_desde = self.request.POST['bloqueo_por_periodo_fecha_desde']
            fecha_hasta = self.request.POST['bloqueo_por_periodo_fecha_hasta']
            motivo_bloqueo_id = \
                self.request.POST['bloqueo_por_periodo_motivo_bloqueo']
            observaciones = \
                self.request.POST['bloqueo_por_periodo_observaciones']

            if not fecha_desde or not fecha_hasta or not motivo_bloqueo_id:

                messages.add_message(
                    request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

                return HttpResponseRedirect(
                    '/agendas/bloqueo/' + str(agenda.id))

            validacion = self.validar_fechas_por_periodo(
                agenda, fecha_desde, fecha_hasta)

            if not validacion['ok']:
                messages.add_message(
                    request, messages.ERROR, validacion['mensaje'])

                return HttpResponseRedirect(
                    '/agendas/bloqueo/' + str(agenda.id))

            motivo_bloqueo = MotivoBloqueo.objects.get(pk=motivo_bloqueo_id)

            bloqueo = AgendaPeriodoBloqueo.objects.create(
                agenda=agenda,
                fecha_desde=validacion['fecha_desde'],
                fecha_hasta=validacion['fecha_hasta'],
                motivo_bloqueo=motivo_bloqueo,
                observacion=observaciones
                )

            self.bloquear_fechas_detalle_por_periodo(bloqueo)

            messages.add_message(
                request, messages.ERROR, 'PERIODO BLOQUEADO')

            return HttpResponseRedirect(
                '/agendas/bloqueo/' + str(agenda.id))

    def validar_fechas_por_periodo(self, agenda, fecha_desde, fecha_hasta):

        validacion = {
            'ok': True,
            'mensaje': '',
            'fecha_desde': 0,
            'fecha_hasta': 0
            }

        try:
            fecha_desde = datetime.datetime.strptime(fecha_desde, '%d/%m/%Y')
            fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%d/%m/%Y')
        except:
            validacion['ok'] = False
            validacion['mensaje'] = \
                    'EL FORMULARIO CONTIENE ERRORES. FECHAS NO VALIDAS'
            return validacion

        if (fecha_desde.date() < agenda.fecha_desde or
                fecha_hasta.date() > agenda.fecha_hasta):

            validacion['ok'] = False
            validacion['mensaje'] = \
                'EL FORMULARIO CONTIENE ERRORES. VERIFICAR RANGOS DE FECHAS'
            return validacion

        validacion['fecha_desde'] = fecha_desde
        validacion['fecha_hasta'] = fecha_hasta

        return validacion

    def bloquear_fechas_detalle_por_periodo(self, bloqueo):

        listado_fechas = AgendaFechaDetalle.objects.filter(
            agenda=bloqueo.agenda,
            fecha__range=[bloqueo.fecha_desde, bloqueo.fecha_hasta]
            )

        for fecha_detalle in listado_fechas:
            try:
                fecha_bloqueo = AgendaFechaDetalleBloqueo.objects.get(
                    fecha_detalle=fecha_detalle)
                fecha_bloqueo.motivo_bloqueo = bloqueo.motivo_bloqueo
                fecha_bloqueo.observacion = bloqueo.observacion
                fecha_bloqueo.save()
            except:
                AgendaFechaDetalleBloqueo.objects.create(
                    agenda=bloqueo.agenda,
                    dia_configuracion=fecha_detalle.dia_configuracion,
                    fecha_detalle=fecha_detalle,
                    motivo_bloqueo=bloqueo.motivo_bloqueo,
                    observacion=bloqueo.observacion
                    )


class AgendaPeriodoBloqueoDelete(DeleteView):

    model = AgendaPeriodoBloqueo
    template_name = 'agendas/agenda_bloqueos_delete.html'

    def post(self, request, *args, **kwargs):

        bloqueo = AgendaPeriodoBloqueo.objects.get(pk=kwargs['pk'])
        agenda_id = bloqueo.agenda.id

        self.borrar_fechas_detalle_bloqueo(bloqueo)
        self.borrar_dias_configuracion_bloqueo(bloqueo)

        bloqueo.delete()

        return HttpResponseRedirect('/agendas/bloqueo/' + str(agenda_id))

    def borrar_fechas_detalle_bloqueo(self, bloqueo):

        listado_fechas_bloqueadas = AgendaFechaDetalleBloqueo.objects.filter(
            agenda=bloqueo.agenda,
            fecha_detalle__fecha__range=[
                bloqueo.fecha_desde, bloqueo.fecha_hasta]
            )

        for fecha_bloqueo in listado_fechas_bloqueadas:
            fecha_bloqueo.delete()

    def borrar_dias_configuracion_bloqueo(self, bloqueo):

        listado_bloqueos = AgendaDiaConfiguracionBloqueo.objects.filter(
            agenda=bloqueo.agenda,
            fecha_desde__range=[bloqueo.fecha_desde, bloqueo.fecha_hasta],
            fecha_hasta__range=[bloqueo.fecha_desde, bloqueo.fecha_hasta],
            )

        for dia_configuracion_bloqueo in listado_bloqueos:
            dia_configuracion_bloqueo.delete()


class AgendaFechaDetalleBloqueoDelete(DeleteView):

    model = AgendaFechaDetalleBloqueo
    template_name = 'agendas/agenda_bloqueos_delete.html'

    def dispatch(self, *args, **kwargs):
        self.fecha_bloqueo = AgendaFechaDetalleBloqueo.objects.get(
            id=kwargs['pk'])
        self.agenda_id = self.fecha_bloqueo.agenda.id
        return super(AgendaFechaDetalleBloqueoDelete, self).dispatch(
                *args, **kwargs)

    def get_success_url(self):
        return '/agendas/bloqueo/' + str(self.agenda_id)


class AgendaDiaConfiguracionBloqueoCreate(CreateView):

    form_class = AgendaDiaConfiguracionBloqueoForm
    model = AgendaDiaConfiguracionBloqueo
    template_name = 'agendas/agenda_bloqueos_dia_configuracion.html'

    def get(self, request, *args, **kwargs):

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=kwargs['pk'])

        form = AgendaDiaConfiguracionBloqueoForm()

        return render_to_response(
            'agendas/agenda_bloqueos_dia_configuracion.html',
            {'form': form, 'configuracion': dia_configuracion},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        form = AgendaDiaConfiguracionBloqueoForm(self.request.POST)

        if form.is_valid():

            dia_configuracion_bloqueo = form.save()

            self.bloquear_fechas_detalle(dia_configuracion_bloqueo)

            messages.add_message(
                request, messages.SUCCESS, 'BLOQUEO AGREGADO')

            return HttpResponseRedirect(
                '/agendas/bloqueo/' + str(dia_configuracion_bloqueo.agenda.id))

        dia_configuracion = AgendaDiaConfiguracion.objects.get(
            pk=kwargs['pk'])

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'agendas/agenda_bloqueos_dia_configuracion.html',
            {'form': form, 'configuracion': dia_configuracion},
            context_instance=RequestContext(request)
        )

    def bloquear_fechas_detalle(self, bloqueo):

        listado_fechas = AgendaFechaDetalle.objects.filter(
            agenda=bloqueo.agenda,
            dia_configuracion=bloqueo.dia_configuracion,
            fecha__range=[bloqueo.fecha_desde, bloqueo.fecha_hasta]
            )

        for fecha_detalle in listado_fechas:
            try:
                fecha_bloqueo = AgendaFechaDetalleBloqueo.objects.get(
                    fecha_detalle=fecha_detalle
                    )
                fecha_bloqueo.motivo_bloqueo = bloqueo.motivo_bloqueo
                fecha_bloqueo.observacion = bloqueo.observacion
                fecha_bloqueo.save()
            except:
                AgendaFechaDetalleBloqueo.objects.create(
                    agenda=bloqueo.agenda,
                    dia_configuracion=bloqueo.dia_configuracion,
                    fecha_detalle=fecha_detalle,
                    motivo_bloqueo=bloqueo.motivo_bloqueo,
                    observacion=bloqueo.observacion
                    )


class AgendaDiaConfiguracionBloqueoDelete(DeleteView):

    model = AgendaDiaConfiguracionBloqueo
    template_name = 'agendas/agenda_bloqueos_delete.html'

    def post(self, request, *args, **kwargs):

        config_bloqueo = AgendaDiaConfiguracionBloqueo.objects.get(
            pk=kwargs['pk'])

        agenda_id = config_bloqueo.agenda.id

        self.borrar_fechas_detalle_bloqueo(config_bloqueo)

        config_bloqueo.delete()

        return HttpResponseRedirect('/agendas/bloqueo/' + str(agenda_id))

    def borrar_fechas_detalle_bloqueo(self, config_bloqueo):

        listado_fechas_bloqueadas = AgendaFechaDetalleBloqueo.objects.filter(
            agenda=config_bloqueo.agenda,
            dia_configuracion=config_bloqueo.dia_configuracion,
            fecha_detalle__fecha__range=[
                config_bloqueo.fecha_desde, config_bloqueo.fecha_hasta]
            )

        for fecha_bloqueo in listado_fechas_bloqueadas:
            fecha_bloqueo.delete()


# ----------------------------
# EXTENSION DE AGENDA
# ----------------------------

class AgendaExtension(UpdateView):

    model = Agenda

    def get(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])

        return render_to_response(
            'agendas/agenda_extension.html',
            {'agenda': agenda},
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        agenda = Agenda.objects.get(pk=kwargs['pk'])
        fecha_hasta = self.request.POST.get('fecha_hasta', None)

        if not fecha_hasta:

            messages.add_message(
                request, messages.ERROR,
                'EL FORMULARIO CONTIENE ERRORES. INTRODUZCA FECHA VALIDA'
                )

            return HttpResponseRedirect('/agendas/extender/' + str(agenda.id))

        validacion = self.validar_fecha(agenda, fecha_hasta)

        if not validacion['ok']:
            messages.add_message(
                request, messages.ERROR, validacion['mensaje'])

            return HttpResponseRedirect('/agendas/extender/' + str(agenda.id))

        self.extender_dependencias(agenda, validacion['fecha'])

        agenda.fecha_hasta = validacion['fecha']
        agenda.save()

        messages.add_message(
            request, messages.INFO, 'AGENDA EXTENDIDA CON EXITO!!')

        return HttpResponseRedirect('/agendas/extender/' + str(agenda.id))

    def validar_fecha(self, agenda, fecha):

        validacion = {'ok': True, 'mensaje': '', 'fecha': 0}

        try:
            fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        except:
            validacion['ok'] = False
            validacion['mensaje'] = 'FECHA NO VALIDA'
            return validacion

        if fecha.date() < agenda.fecha_hasta:

            validacion['ok'] = False
            validacion['mensaje'] = 'LA FECHA NO DEBE SER MENOR A LA ANTERIOR'
            return validacion

        validacion['fecha'] = fecha

        return validacion

    def extender_dependencias(self, agenda, fecha):

        listado_dias_configuracion = AgendaDiaConfiguracion.objects.filter(
            agenda=agenda, fecha_hasta=agenda.fecha_hasta)

        for dia_configuracion in listado_dias_configuracion:
            self.generar_fechas_detalle(dia_configuracion, fecha)
            dia_configuracion.fecha_hasta = fecha
            dia_configuracion.save()

    def generar_fechas_detalle(self, dia_configuracion, fecha):

        fecha_desde = datetime.datetime.strptime(
            str(dia_configuracion.fecha_hasta), '%Y-%m-%d')

        fecha_desde += datetime.timedelta(days=1)

        if (dia_configuracion.dia.numero == fecha_desde.weekday()):
            self.guardar_fecha_detalle(fecha_desde, dia_configuracion)

        cantidad_dias = helpers.get_cantidad_dias_entre_fechas(
            fecha_desde.date(), fecha.date())

        cantidad_dias += 1  # se suma 1 para que abarque hasta fecha_hasta

        for dia_siguiente in range(1, cantidad_dias):
            fecha = fecha_desde + datetime.timedelta(days=dia_siguiente)
            if (dia_configuracion.dia.numero == fecha.weekday()):
                self.guardar_fecha_detalle(fecha, dia_configuracion)

    def guardar_fecha_detalle(self, fecha, dia_configuracion):

        AgendaFechaDetalle.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha=fecha,
            hora_desde=dia_configuracion.hora_desde,
            hora_hasta=dia_configuracion.hora_hasta,
            duracion_minutos=dia_configuracion.duracion_minutos,
            practica=dia_configuracion.practica
            )
