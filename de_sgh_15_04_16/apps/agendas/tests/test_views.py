# -*- coding: utf-8 -*-

import datetime

from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.complementos.salud.models import Especialidad, Practica
from apps.empleados.models import Empleado
from apps.instituciones.models import Institucion
from apps.personas.models import Persona
from apps.seguridad.models import EmpleadoAgenda

from apps.agendas.models import (Agenda, AgendaDiaConfiguracion, TipoAgenda,
                                 Dia, AgendaFechaDetalle,
                                 AgendaDiaConfiguracionBloqueo, MotivoBloqueo,
                                 AgendaFechaDetalleBloqueo,
                                 AgendaPeriodoBloqueo)
from apps.agendas.views import (AgendaListView, AgendaDiaConfiguracionCreate,
                                AgendaDiaConfiguracionBloqueoCreate,
                                AgendaDiaConfiguracionBloqueoDelete,
                                AgendaBloqueoCreate, AgendaPeriodoBloqueoDelete,
                                AgendaExtension)


# ---------------- HELPERS TEST ----------------


def generar_agenda():

    persona = Persona.objects.create(apellido='perez', nombre='juan')
    empleado = Empleado.objects.create(persona=persona)

    EmpleadoAgenda.objects.create(empleado=empleado, tiene_agenda=True)

    especialidad = Especialidad.objects.create(nombre='Oncologia')

    pais = Pais.objects.create(nombre='Argentina')
    provincia = Provincia.objects.create(nombre='Formosa', pais=pais)
    departamento = Departamento.objects.create(nombre='Pilcomayo',
                                               provincia=provincia)

    tipo_agenda = TipoAgenda.objects.create(descripcion='Programada')

    institucion = Institucion.objects.create(
        nombre='HAC', cuit='10101010', pais=pais,
        provincia=provincia, departamento=departamento)

    Agenda.objects.create(
        institucion=institucion,
        profesional=empleado,
        fecha_desde='2015-11-01',
        fecha_hasta='2015-12-31',
        especialidad=especialidad,
        tipo_agenda=tipo_agenda
    )


def generar_dia_configuracion(agenda):

    dia = Dia.objects.create(nombre='Lunes', numero=0)

    AgendaDiaConfiguracion.objects.create(
        agenda=agenda,
        dia=dia,
        fecha_desde='2015-11-01',
        fecha_hasta='2015-11-18',
        hora_desde='08:00:00',
        hora_hasta='12:00:00',
        duracion_minutos=15
        )


def generar_fecha_detalle(dia_configuracion):

    dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)

    AgendaFechaDetalle.objects.create(
        agenda=dia_configuracion.agenda,
        dia_configuracion=dia_configuracion,
        fecha='2015-11-02',
        hora_desde=dia_configuracion.hora_desde,
        hora_hasta=dia_configuracion.hora_hasta,
        duracion_minutos=dia_configuracion.duracion_minutos,
        practica=dia_configuracion.practica
        )

    AgendaFechaDetalle.objects.create(
        agenda=dia_configuracion.agenda,
        dia_configuracion=dia_configuracion,
        fecha='2015-11-09',
        hora_desde=dia_configuracion.hora_desde,
        hora_hasta=dia_configuracion.hora_hasta,
        duracion_minutos=dia_configuracion.duracion_minutos,
        practica=dia_configuracion.practica
        )

    AgendaFechaDetalle.objects.create(
        agenda=dia_configuracion.agenda,
        dia_configuracion=dia_configuracion,
        fecha='2015-11-16',
        hora_desde=dia_configuracion.hora_desde,
        hora_hasta=dia_configuracion.hora_hasta,
        duracion_minutos=dia_configuracion.duracion_minutos,
        practica=dia_configuracion.practica
        )


# ---------------- TEST CASES ----------------


class AgendaListViewTestCase(TestCase):

    def test_buscar_por_profesional(self):

        generar_agenda()

        self.sut = AgendaListView()

        persona = Persona.objects.create(apellido='Lopez', nombre='Sandra')
        empleado = Empleado.objects.create(persona=persona)

        result = self.sut.buscar_por_profesional(empleado.id)
        self.assertEqual(0, len(result))

        empleado = Empleado.objects.get(pk=1)

        result = self.sut.buscar_por_profesional(empleado.id)
        self.assertEqual(1, len(result))
        self.assertEqual('perez', empleado.persona.apellido)

    def test_buscar_por_especialidad(self):

        generar_agenda()

        self.sut = AgendaListView()

        especialidad = Especialidad.objects.create(nombre='Cardiologia')

        result = self.sut.buscar_por_especialidad(especialidad.id)
        self.assertEqual(0, len(result))

        especialidad = Especialidad.objects.get(pk=1)

        result = self.sut.buscar_por_especialidad(especialidad.id)
        self.assertEqual(1, len(result))
        self.assertEqual('Oncologia', especialidad.nombre)

    def test_buscar_por_tipo_agenda(self):

        generar_agenda()

        self.sut = AgendaListView()

        tipo_agenda = TipoAgenda.objects.create(descripcion='Inmediata')

        result = self.sut.buscar_por_tipo_agenda(tipo_agenda.id)
        self.assertEqual(0, len(result))

        tipo_agenda = TipoAgenda.objects.get(pk=1)

        result = self.sut.buscar_por_tipo_agenda(tipo_agenda.id)
        self.assertEqual(1, len(result))
        self.assertEqual('Programada', tipo_agenda.descripcion)


class AgendaDiaConfiguracionCreateTestCase(TestCase):

    def test_generar_fechas_agenda(self):

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        especialidad = Especialidad.objects.get(pk=1)

        dia_lunes = Dia.objects.create(nombre='Lunes', numero=0)
        practica = Practica.objects.create(
            especialidad=especialidad, nombre='Practica1')

        dia_config = AgendaDiaConfiguracion.objects.create(
            agenda=agenda,
            dia=dia_lunes,
            fecha_desde='2015-11-02',
            fecha_hasta='2015-11-30',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15,
            practica=practica,
        )

        agenda_dia_configuracion_create = AgendaDiaConfiguracionCreate()
        agenda_dia_configuracion_create.generar_fechas_agenda(dia_config)
        result = AgendaFechaDetalle.objects.all()

        # Dias Lunes entre el 02/11/2015 y el 30/11/2015
        # 02/11/2015, 09/11/2015, 16/11/2015, 23/11/2015 y 30/11/2015

        self.assertEqual(5, len(result))

        listado_fechas = [
            '2015-11-02', '2015-11-09', '2015-11-16',
            '2015-11-23', '2015-11-30'
            ]

        for i, fecha in enumerate(listado_fechas):
            fecha = datetime.datetime.strptime(str(fecha), '%Y-%m-%d').date()
            self.assertEqual(fecha, result[i].fecha)


class AgendaDiaConfiguracionBloqueoCreateTestCase(TestCase):

    def test_bloquear_fechas_detalle(self):

        listado = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(0, len(listado))

        sut = AgendaDiaConfiguracionBloqueoCreate()

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        generar_fecha_detalle(dia_configuracion)

        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')
        motivo_bloqueo_licencia = MotivoBloqueo.objects.create(
            descripcion='Licencia')

        fechas = [
            datetime.datetime.strptime('2015-11-02', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2015-11-09', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2015-11-16', '%Y-%m-%d').date(),
            ]

        # bloqueo por dia configuracion
        bloqueo = AgendaDiaConfiguracionBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_desde='2015-11-02',
            fecha_hasta='2015-11-12',
            motivo_bloqueo=motivo_bloqueo
            )

        sut.bloquear_fechas_detalle(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()

        self.assertEqual(2, len(listado_bloqueos))
        self.assertEqual(fechas[0], listado_bloqueos[0].fecha_detalle.fecha)
        self.assertEqual(fechas[1], listado_bloqueos[1].fecha_detalle.fecha)

        AgendaFechaDetalleBloqueo.objects.all().delete()
        bloqueo.fecha_hasta = '2015-11-05'
        sut.bloquear_fechas_detalle(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()

        self.assertEqual(1, len(listado_bloqueos))
        self.assertEqual(fechas[0], listado_bloqueos[0].fecha_detalle.fecha)

        AgendaFechaDetalleBloqueo.objects.all().delete()
        bloqueo.fecha_desde = '2015-11-10'
        bloqueo.fecha_hasta = '2015-11-18'
        sut.bloquear_fechas_detalle(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()

        self.assertEqual(1, len(listado_bloqueos))
        self.assertEqual(fechas[2], listado_bloqueos[0].fecha_detalle.fecha)

        # se agrega una fecha bloqueada
        # si ya existe bloqueo para una fecha, entonces se modifica solo el
        # motivo y la observacion
        AgendaFechaDetalleBloqueo.objects.all().delete()
        fecha_detalle = AgendaFechaDetalle.objects.get(pk=2)

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle,
            motivo_bloqueo=motivo_bloqueo_licencia,
            observacion='OBS ORIGINAL'
            )

        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(1, len(listado_bloqueos))
        self.assertEqual(fechas[1], listado_bloqueos[0].fecha_detalle.fecha)
        self.assertEqual(
            'Licencia', listado_bloqueos[0].motivo_bloqueo.descripcion)
        self.assertEqual('OBS ORIGINAL', listado_bloqueos[0].observacion)

        bloqueo.fecha_desde = '2015-11-02'
        bloqueo.fecha_hasta = '2015-11-20'
        bloqueo.observacion = 'NUEVA OBS'
        sut.bloquear_fechas_detalle(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()

        self.assertEqual(3, len(listado_bloqueos))
        self.assertEqual(fechas[1], listado_bloqueos[0].fecha_detalle.fecha)
        self.assertEqual(
            'Feriado', listado_bloqueos[1].motivo_bloqueo.descripcion)
        self.assertEqual(
            'NUEVA OBS', listado_bloqueos[1].observacion)


class AgendaDiaConfiguracionBloqueoDeleteTestCase(TestCase):

    def test_borrar_fechas_detalle_bloqueo(self):

        listado = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(0, len(listado))

        sut = AgendaDiaConfiguracionBloqueoDelete()

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        generar_fecha_detalle(dia_configuracion)

        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')
        fecha_detalle_1 = AgendaFechaDetalle.objects.get(pk=1)
        fecha_detalle_2 = AgendaFechaDetalle.objects.get(pk=2)

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle_1,
            motivo_bloqueo=motivo_bloqueo,
            observacion='OBS ORIGINAL'
            )

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle_2,
            motivo_bloqueo=motivo_bloqueo,
            observacion='OBS ORIGINAL'
            )

        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(2, len(listado_bloqueos))

        bloqueo = AgendaDiaConfiguracionBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_desde='2015-11-02',
            fecha_hasta='2015-11-12',
            motivo_bloqueo=motivo_bloqueo
            )

        sut.borrar_fechas_detalle_bloqueo(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(0, len(listado_bloqueos))


class AgendaBloqueoCreateTestCase(TestCase):

    def test_bloquear_fechas_detalle_por_periodo(self):

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        generar_fecha_detalle(dia_configuracion)

        sut = AgendaBloqueoCreate()

        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')

        bloqueo = AgendaPeriodoBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            fecha_desde='2015-11-05',
            fecha_hasta='2015-11-20',
            motivo_bloqueo=motivo_bloqueo
            )

        sut.bloquear_fechas_detalle_por_periodo(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        listado_fechas = ['2015-11-09', '2015-11-16']

        self.assertEqual(2, len(listado_bloqueos))

        for i, fecha in enumerate(listado_fechas):
            fecha = datetime.datetime.strptime(str(fecha), '%Y-%m-%d').date()
            self.assertEqual(fecha, listado_bloqueos[i].fecha_detalle.fecha)

        AgendaFechaDetalleBloqueo.objects.all().delete()
        fecha_detalle = AgendaFechaDetalle.objects.get(pk=1)

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle,
            motivo_bloqueo=motivo_bloqueo
            )

        sut.bloquear_fechas_detalle_por_periodo(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        listado_fechas = ['2015-11-02', '2015-11-09', '2015-11-16']

        self.assertEqual(3, len(listado_bloqueos))

        for i, fecha in enumerate(listado_fechas):
            fecha = datetime.datetime.strptime(str(fecha), '%Y-%m-%d').date()
            self.assertEqual(fecha, listado_bloqueos[i].fecha_detalle.fecha)

    def test_validar_fechas_por_periodo(self):

        generar_agenda()
        agenda = Agenda.objects.get(pk=1)

        sut = AgendaBloqueoCreate()

        fecha_desde = '10/11/2015'
        fecha_hasta = '30/11/2015'
        result = sut.validar_fechas_por_periodo(
            agenda, fecha_desde, fecha_hasta)

        self.assertTrue(result['ok'])

        fecha_desde = '10/10/2015'
        fecha_hasta = '30/11/2015'
        result = sut.validar_fechas_por_periodo(
            agenda, fecha_desde, fecha_hasta)

        self.assertFalse(result['ok'])
        self.assertEqual(
            'EL FORMULARIO CONTIENE ERRORES. VERIFICAR RANGOS DE FECHAS',
            result['mensaje']
            )

        fecha_desde = 'aaaaaaa'
        fecha_hasta = '30/11/2015'
        result = sut.validar_fechas_por_periodo(
            agenda, fecha_desde, fecha_hasta)

        self.assertFalse(result['ok'])
        self.assertEqual(
            'EL FORMULARIO CONTIENE ERRORES. FECHAS NO VALIDAS',
            result['mensaje']
            )


class AgendaPeriodoBloqueoDeleteTestCase(TestCase):

    def test_borrar_fechas_detalle_bloqueo(self):

        listado = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(0, len(listado))

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        generar_fecha_detalle(dia_configuracion)

        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')
        fecha_detalle_1 = AgendaFechaDetalle.objects.get(pk=1)
        fecha_detalle_2 = AgendaFechaDetalle.objects.get(pk=2)

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle_1,
            motivo_bloqueo=motivo_bloqueo,
            observacion='OBS ORIGINAL'
            )

        AgendaFechaDetalleBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_detalle=fecha_detalle_2,
            motivo_bloqueo=motivo_bloqueo,
            observacion='OBS ORIGINAL'
            )

        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(2, len(listado_bloqueos))

        bloqueo = AgendaPeriodoBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            fecha_desde='2015-11-02',
            fecha_hasta='2015-11-12',
            motivo_bloqueo=motivo_bloqueo
            )

        sut = AgendaPeriodoBloqueoDelete()

        sut.borrar_fechas_detalle_bloqueo(bloqueo)
        listado_bloqueos = AgendaFechaDetalleBloqueo.objects.all()
        self.assertEqual(0, len(listado_bloqueos))

    def test_borrar_dias_configuracion_bloqueo(self):

        listado = AgendaDiaConfiguracionBloqueo.objects.all()
        self.assertEqual(0, len(listado))

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')

        AgendaDiaConfiguracionBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            dia_configuracion=dia_configuracion,
            fecha_desde='2015-11-02',
            fecha_hasta='2015-11-12',
            motivo_bloqueo=motivo_bloqueo
            )

        listado_bloqueos = AgendaDiaConfiguracionBloqueo.objects.all()
        self.assertEqual(1, len(listado_bloqueos))

        periodo_bloqueo = AgendaPeriodoBloqueo.objects.create(
            agenda=dia_configuracion.agenda,
            fecha_desde='2015-12-01',
            fecha_hasta='2015-12-20',
            motivo_bloqueo=motivo_bloqueo
            )

        sut = AgendaPeriodoBloqueoDelete()

        sut.borrar_dias_configuracion_bloqueo(periodo_bloqueo)
        listado_bloqueos = AgendaDiaConfiguracionBloqueo.objects.all()
        self.assertEqual(1, len(listado_bloqueos))

        periodo_bloqueo.fecha_desde = '2015-11-01'
        periodo_bloqueo.fecha_hasta = '2015-11-30'

        sut.borrar_dias_configuracion_bloqueo(periodo_bloqueo)
        listado_bloqueos = AgendaDiaConfiguracionBloqueo.objects.all()
        self.assertEqual(0, len(listado_bloqueos))


class AgendaExtensionTestCase(TestCase):

    def test_validar_fecha(self):

        generar_agenda()
        agenda = Agenda.objects.get(pk=1)

        agenda_extension = AgendaExtension()

        fecha_hasta = '30/12/2015'
        result = agenda_extension.validar_fecha(agenda, fecha_hasta)
        self.assertFalse(result['ok'])
        self.assertEqual(
            'LA FECHA NO DEBE SER MENOR A LA ANTERIOR', result['mensaje'])

        fecha_hasta = '31/12/2015'
        result = agenda_extension.validar_fecha(agenda, fecha_hasta)
        self.assertTrue(result['ok'])

        fecha_hasta = '01/01/2016'
        result = agenda_extension.validar_fecha(agenda, fecha_hasta)
        self.assertTrue(result['ok'])

        fecha_hasta = '--------'
        result = agenda_extension.validar_fecha(agenda, fecha_hasta)
        self.assertFalse(result['ok'])
        self.assertEqual('FECHA NO VALIDA', result['mensaje'])

    def test_extender_dependencias(self):

        generar_agenda()
        agenda = Agenda.objects.get(pk=1)

        agenda_extension = AgendaExtension()

        lunes = Dia.objects.create(nombre='Lunes', numero=0)
        martes = Dia.objects.create(nombre='Martes', numero=0)

        AgendaDiaConfiguracion.objects.create(
            agenda=agenda,
            dia=lunes,
            fecha_desde='2015-11-01',
            fecha_hasta='2015-11-18',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15
            )

        AgendaDiaConfiguracion.objects.create(
            agenda=agenda,
            dia=lunes,
            fecha_desde='2015-11-01',
            fecha_hasta='2015-12-31',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15
            )

        AgendaDiaConfiguracion.objects.create(
            agenda=agenda,
            dia=martes,
            fecha_desde='2015-11-01',
            fecha_hasta='2015-12-31',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15
            )

        fecha = datetime.datetime.strptime('01/02/2016', '%d/%m/%Y')

        fechas_hasta = [
            datetime.datetime.strptime('2015-11-18', '%Y-%m-%d').date(),
            fecha.date(),
            fecha.date()
            ]

        agenda_extension.extender_dependencias(agenda, fecha)
        listado_dias = AgendaDiaConfiguracion.objects.filter(agenda=agenda)

        for i, dia_configuracion in enumerate(listado_dias):
            self.assertEqual(fechas_hasta[i], dia_configuracion.fecha_hasta)

    def test_generar_fechas_detalle(self):

        generar_agenda()
        agenda = Agenda.objects.get(pk=1)

        agenda_extension = AgendaExtension()

        viernes = Dia.objects.create(nombre='Viernes', numero=4)

        dia_configuracion = AgendaDiaConfiguracion.objects.create(
            agenda=agenda,
            dia=viernes,
            fecha_desde='2015-11-01',
            fecha_hasta='2015-12-31',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15
            )

        fecha = datetime.datetime.strptime('15/01/2016', '%d/%m/%Y')
        agenda_extension.generar_fechas_detalle(dia_configuracion, fecha)
        listado_fechas = AgendaFechaDetalle.objects.all()

        fechas = [
            datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2016-01-08', '%Y-%m-%d').date(),
            datetime.datetime.strptime('2016-01-15', '%Y-%m-%d').date()
            ]

        for i, fecha_detalle in enumerate(listado_fechas):
            self.assertEqual(fechas[i], fecha_detalle.fecha)
