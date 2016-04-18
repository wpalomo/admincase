
from datetime import datetime

from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.complementos.salud.models import Especialidad
from apps.empleados.models import Empleado
from apps.instituciones.models import Institucion
from apps.personas.models import Persona
from apps.seguridad.models import EmpleadoAgenda

from apps.agendas.forms import (AgendaForm, AgendaDiaConfiguracionForm,
                                AgendaFechaDetalleForm,
                                AgendaDiaConfiguracionBloqueoForm)
from apps.agendas.models import (Agenda, TipoAgenda, Dia, MotivoBloqueo,
                                 AgendaDiaConfiguracion)


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


# ---------------- TEST CASES ----------------


class AgendaFormTestCase(TestCase):

    def setUp(self):

        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)

        EmpleadoAgenda.objects.create(empleado=empleado, tiene_agenda=True)

        pais = Pais.objects.create(nombre='Argentina')
        provincia = Provincia.objects.create(nombre='Formosa', pais=pais)
        departamento = Departamento.objects.create(nombre='Pilcomayo',
                                                   provincia=provincia)

        Especialidad.objects.create(nombre='Oncologia')
        TipoAgenda.objects.create(descripcion='Porgramada')

        Institucion.objects.create(nombre='HAC', cuit='10101010', pais=pais,
            provincia=provincia, departamento=departamento)

    def tearDown(self):
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        EmpleadoAgenda.objects.all().delete()
        Pais.objects.all().delete()
        Provincia.objects.all().delete()
        Departamento.objects.all().delete()
        Especialidad.objects.all().delete()
        TipoAgenda.objects.all().delete()
        Institucion.objects.all().delete()

    def test_form(self):

        form = AgendaForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        institucion = Institucion.objects.get(pk=1)
        empleado = Empleado.objects.get(pk=1)
        especialidad = Especialidad.objects.get(pk=1)
        tipo_agenda = TipoAgenda.objects.get(pk=1)

        data = {
            'institucion': institucion.id,
            'profesional': empleado.id,
            'fecha_desde': datetime.now(),
            'fecha_hasta': datetime.now(),
            'especialidad': especialidad.id,
            'tipo_agenda': tipo_agenda.id
        }

        form = AgendaForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    def test_fechas(self):

        institucion = Institucion.objects.get(pk=1)
        empleado = Empleado.objects.get(pk=1)
        especialidad = Especialidad.objects.get(pk=1)
        tipo_agenda = TipoAgenda.objects.get(pk=1)

        data = {
            'institucion': institucion.id,
            'profesional': empleado.id,
            'fecha_desde': datetime.now(),
            'fecha_hasta': datetime.now(),
            'especialidad': especialidad.id,
            'tipo_agenda': tipo_agenda.id
        }

        form = AgendaForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

        data['fecha_hasta'] = '05/01/2000'
        form = AgendaForm(data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        data['fecha_hasta'] = '05/11/2030'
        form = AgendaForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class AgendaDiaConfiguracionFormTestCase(TestCase):

    def test_form(self):

        generar_agenda()

        especialidad = Especialidad.objects.get(pk=1)

        form = AgendaDiaConfiguracionForm(especialidad.id)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        dia = Dia.objects.create(nombre='Lunes', numero=0)
        agenda = Agenda.objects.get(pk=1)

        data = {
            'agenda': agenda.id,
            'dia': dia.id,
            'fecha_desde': '01/11/2015',
            'fecha_hasta': '01/12/2015',
            'hora_desde': '08:00:00',
            'hora_hasta': '12:00:00',
            'duracion_minutos': 15
            }

        form = AgendaDiaConfiguracionForm(especialidad.id, data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class AgendaFechaDetalleFormTestCase(TestCase):

    def test_form(self):

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        especialidad = Especialidad.objects.get(pk=1)

        form = AgendaFechaDetalleForm(especialidad.id)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        agenda = Agenda.objects.get(pk=1)
        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)

        data = {
            'agenda': agenda.id,
            'dia_configuracion': dia_configuracion.id,
            'fecha': '10/11/2015',
            'hora_desde': '08:00:00',
            'hora_hasta': '10:00:00',
            'duracion_minutos': 20
            }

        form = AgendaFechaDetalleForm(especialidad.id, data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class AgendaDiaConfiguracionBloqueoFormTestCase(TestCase):

    def test_form(self):

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        form = AgendaDiaConfiguracionBloqueoForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        dia_configuracion = AgendaDiaConfiguracion.objects.get(pk=1)
        motivo_bloqueo = MotivoBloqueo.objects.create(descripcion='Feriado')

        data = {
            'agenda': agenda.id,
            'dia_configuracion': dia_configuracion.id,
            'fecha_desde': '01/11/2015',
            'fecha_hasta': '10/11/2015',
            'motivo_bloqueo': motivo_bloqueo.id
            }

        form = AgendaDiaConfiguracionBloqueoForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())