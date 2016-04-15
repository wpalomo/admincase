
import ast
from datetime import datetime

from django.http import HttpRequest
from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.complementos.salud.models import Especialidad
from apps.empleados.models import Empleado, EmpleadoEspecialidad
from apps.instituciones.models import Institucion
from apps.personas.models import Persona
from apps.seguridad.models import EmpleadoAgenda

from apps.agendas import helpers
from apps.agendas.models import Agenda, AgendaDiaConfiguracion, TipoAgenda, Dia


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


class HelpersTestCase(TestCase):

    def test_hay_superposicion_fecha_hora(self):

        generar_agenda()

        agenda = Agenda.objects.get(pk=1)
        generar_dia_configuracion(agenda)

        agenda = Agenda.objects.get(pk=1)
        dia_lunes = Dia.objects.get(numero=0)

        dia_config = AgendaDiaConfiguracion(
            agenda=agenda,
            dia=dia_lunes,
            fecha_desde='2015-09-30',
            fecha_hasta='2015-11-23',
            hora_desde='08:00:00',
            hora_hasta='12:00:00',
            duracion_minutos=15
        )

        result = helpers.hay_superposicion_fecha_hora(dia_config)
        self.assertTrue(result)

        dia_config.fecha_desde = '2015-10-15'
        dia_config.fecha_hasta = '2015-11-25'

        result = helpers.hay_superposicion_fecha_hora(dia_config)
        self.assertTrue(result)

        dia_config.fecha_desde = '2015-10-22'
        dia_config.fecha_hasta = '2015-10-30'

        result = helpers.hay_superposicion_fecha_hora(dia_config)
        self.assertFalse(result)

        dia_config.fecha_desde = '2015-09-25'
        dia_config.fecha_hasta = '2015-09-30'

        result = helpers.hay_superposicion_fecha_hora(dia_config)
        self.assertFalse(result)

        dia_config.fecha_desde = '2015-09-25'
        dia_config.fecha_hasta = '2015-11-01'

        result = helpers.hay_superposicion_fecha_hora(dia_config)
        self.assertTrue(result)

    def test_hay_superposicion_fecha(self):

        fechas_1 = {'fecha_desde': '2015-09-30', 'fecha_hasta': '2015-10-23'}
        fechas_2 = {'fecha_desde': '2015-10-01', 'fecha_hasta': '2015-10-20'}

        result = helpers.hay_superposicion_fecha(fechas_1, fechas_2)
        self.assertTrue(result)

        fechas_1['fecha_desde'] = '2015-10-15'
        fechas_1['fecha_hasta'] = '2015-10-25'

        result = helpers.hay_superposicion_fecha(fechas_1, fechas_2)
        self.assertTrue(result)

        fechas_1['fecha_desde'] = '2015-10-22'
        fechas_1['fecha_hasta'] = '2015-10-30'

        result = helpers.hay_superposicion_fecha(fechas_1, fechas_2)
        self.assertFalse(result)

        fechas_1['fecha_desde'] = '2015-09-25'
        fechas_1['fecha_hasta'] = '2015-09-30'

        result = helpers.hay_superposicion_fecha(fechas_1, fechas_2)
        self.assertFalse(result)

        fechas_1['fecha_desde'] = '2015-09-25'
        fechas_1['fecha_hasta'] = '2015-10-01'

        result = helpers.hay_superposicion_fecha(fechas_1, fechas_2)
        self.assertTrue(result)

    def test_hay_superposicion_hora(self):

        hora_desde2 = datetime.strptime(str('08:00:00'), '%H:%M:%S').time()
        hora_hasta2 = datetime.strptime(str('12:00:00'), '%H:%M:%S').time()

        horas_1 = {'hora_desde': '08:00:00', 'hora_hasta': '11:00:00'}
        horas_2 = {'hora_desde': hora_desde2, 'hora_hasta': hora_hasta2}

        result = helpers.hay_superposicion_hora(horas_1, horas_2)
        self.assertTrue(result)

        horas_1['hora_desde'] = '07:00:00'
        horas_1['hora_hasta'] = '09:00:00'

        result = helpers.hay_superposicion_hora(horas_1, horas_2)
        self.assertTrue(result)

        horas_1['hora_desde'] = '12:30:00'
        horas_1['hora_hasta'] = '14:00:00'

        result = helpers.hay_superposicion_hora(horas_1, horas_2)
        self.assertFalse(result)

        horas_1['hora_desde'] = '07:00:00'
        horas_1['hora_hasta'] = '07:55:00'

        result = helpers.hay_superposicion_hora(horas_1, horas_2)
        self.assertFalse(result)

        horas_1['hora_desde'] = '11:00:00'
        horas_1['hora_hasta'] = '14:00:00'

        result = helpers.hay_superposicion_hora(horas_1, horas_2)
        self.assertTrue(result)

    def test_get_especialidad_por_profesional(self):

        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)
        especialidad = Especialidad.objects.create(nombre='Oncologia')

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'profesional_id': 1000}

        response = helpers.get_especialidad_por_profesional(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(0, len(result))

        EmpleadoEspecialidad.objects.create(
            empleado=empleado, especialidad=especialidad)

        request.GET = {'profesional_id': 1}
        response = helpers.get_especialidad_por_profesional(request)
        result = self.get_dict_from_response(response)

        self.assertGreater(len(result), 0)
        self.assertIn('nombre', result[0])
        self.assertIn('id', result[0])
        self.assertEqual('Oncologia', result[0]['nombre'])

        especialidad = Especialidad.objects.create(nombre='Cardiologia')
        EmpleadoEspecialidad.objects.create(
            empleado=empleado, especialidad=especialidad)

        response = helpers.get_especialidad_por_profesional(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(2, len(result))
        self.assertEqual('Oncologia', result[0]['nombre'])
        self.assertEqual('Cardiologia', result[1]['nombre'])

    def get_dict_from_response(self, response):
        data_string = response.content.decode("utf-8")
        tipo_transaccion = ast.literal_eval(data_string)

        return tipo_transaccion

    def test_get_cantidad_dias_entre_fechas(self):
        fecha_1 = '2015-01-01'
        fecha_2 = '2015-01-30'

        result = helpers.get_cantidad_dias_entre_fechas(fecha_1, fecha_2)
        self.assertEqual(29, result)

        # Anio 2001 = Febrero tiene 28 dias
        fecha_1 = '2001-02-01'
        fecha_2 = '2001-03-01'

        result = helpers.get_cantidad_dias_entre_fechas(fecha_1, fecha_2)
        self.assertEqual(28, result)

        # Anio 2000 = Bisiesto => Febrero tiene 29 dias
        fecha_1 = '2000-02-01'
        fecha_2 = '2000-03-01'

        result = helpers.get_cantidad_dias_entre_fechas(fecha_1, fecha_2)
        self.assertEqual(29, result)

    def test_hay_superposicion_entre_agendas(self):

        generar_agenda()

        # Se crea una agenda exactamente igual a la generada en el
        # metodo generar_agenda()

        empleado = Empleado.objects.get(pk=1)

        especialidad = Especialidad.objects.get(pk=1)
        institucion = Institucion.objects.get(pk=1)
        tipo_agenda = TipoAgenda.objects.get(pk=1)

        agenda = Agenda(
            institucion=institucion,
            profesional=empleado,
            fecha_desde='2015-11-01',
            fecha_hasta='2015-12-30',
            especialidad=especialidad,
            tipo_agenda=tipo_agenda
        )

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertTrue(result)

        # Pruebas modificando fechas

        agenda.fecha_desde = '2015-10-10'
        agenda.fecha_hasta = '2015-11-20'

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertTrue(result)

        agenda.fecha_desde = '2015-12-28'
        agenda.fecha_hasta = '2016-01-10'

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertTrue(result)

        agenda.fecha_desde = '2015-08-01'
        agenda.fecha_hasta = '2015-09-01'

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertFalse(result)

        agenda.fecha_desde = '2015-07-01'
        agenda.fecha_hasta = '2015-11-05'

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertTrue(result)

        # Pruebas modificando especialidad

        # ------ Configuracion Inicial ------------
        agenda.fecha_desde = '2015-10-01'
        agenda.fecha_hasta = '2015-12-30'
        # -----------------------------------------

        especialidad = Especialidad.objects.create(nombre='Cardiologia')
        agenda.especialidad = especialidad

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertFalse(result)

        # Pruebas modificando profesional

        # ------ Configuracion Inicial ------------
        especialidad = Especialidad.objects.get(pk=1)
        agenda.especialidad = especialidad
        # -----------------------------------------

        persona = Persona.objects.create(apellido='lopez', nombre='juanita')
        empleado = Empleado.objects.create(persona=persona)

        EmpleadoAgenda.objects.create(empleado=empleado, tiene_agenda=True)

        agenda.profesional = empleado

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertFalse(result)

        # Volviendo a configuracion inicial: agenda identica

        # ------ Configuracion Inicial ------------
        empleado = Empleado.objects.get(pk=1)
        agenda.profesional = empleado
        # -----------------------------------------

        result = helpers.hay_superposicion_entre_agendas(agenda)
        self.assertTrue(result)

    def test_get_profesionales_con_agenda(self):

        request = HttpRequest()
        request.method = 'GET'

        response = helpers.get_profesionales_con_agenda(request)
        result = self.get_dict_from_response(response)
        self.assertEqual(0, len(result))

        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)

        EmpleadoAgenda.objects.create(empleado=empleado, tiene_agenda=True)

        response = helpers.get_profesionales_con_agenda(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(1, len(result))
        self.assertEqual('perez, juan', result[0]['nombre'])

    def test_get_especialidades(self):

        request = HttpRequest()
        request.method = 'GET'

        response = helpers.get_especialidades(request)
        result = self.get_dict_from_response(response)
        self.assertEqual(0, len(result))

        Especialidad.objects.create(nombre='Cardiologia')
        Especialidad.objects.create(nombre='Oncologia')

        response = helpers.get_especialidades(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(2, len(result))
        self.assertEqual('Cardiologia', result[0]['nombre'])

    def test_get_tipos_agendas(self):

        request = HttpRequest()
        request.method = 'GET'

        response = helpers.get_tipos_agendas(request)
        result = self.get_dict_from_response(response)
        self.assertEqual(0, len(result))

        TipoAgenda.objects.create(descripcion='Programada')
        TipoAgenda.objects.create(descripcion='Inmediata')

        response = helpers.get_tipos_agendas(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(2, len(result))
        self.assertEqual('Programada', result[0]['descripcion'])