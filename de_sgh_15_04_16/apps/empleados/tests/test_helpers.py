import ast
from datetime import datetime

from django.http import HttpRequest
from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.complementos.persona.models import TipoDocumento, Sexo
from apps.complementos.organigrama.models import (
    Profesion, Cargo, Direccion, Departamento as DepartamentoAsignacion,
    Division, Seccion, Servicio)
from apps.empleados import helpers
from apps.empleados.models import Empleado, AsignacionFormal
from apps.instituciones.models import Institucion
from apps.personas.models import Persona


# --------------------------------------------------------
# TEST Helpers
# --------------------------------------------------------

class HelpersTestCase(TestCase):

    def test_set_nombre_imagen(self):

        archivo = "test_imagen.jpg"
        #id = 1
        numero_documento = 30625184

        #resultado = helpers.cambiar_nombre_imagen(archivo, id)
        resultado = helpers.cambiar_nombre_imagen(archivo, numero_documento)

        fecha = datetime.today()

        fecha_hora_texto = str(fecha.year) + str(fecha.month) + \
                           str(fecha.day) + str(fecha.hour) + \
                           str(fecha.minute) + str(fecha.second)

        nombre = "foto_personal/{documento}_{fecha_nombre}.jpg".format(
            documento=numero_documento, fecha_nombre=fecha_hora_texto)

        self.assertEqual(nombre, resultado)


class HelpersAsignacionFormalTestCase(TestCase):

    def setUp(self):

        self.institucion = self.get_institucion_object()
        self.empleado = self.get_empleado_object()

    def tearDown(self):
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Profesion.objects.all().delete()
        Sexo.objects.all().delete()
        TipoDocumento.objects.all().delete()
        Profesion.objects.all().delete()
        Pais.objects.all().delete()
        Provincia.objects.all().delete()
        Departamento.objects.all().delete()
        Institucion.objects.all().delete()

    def test_get_validar_fechas_historial_asigancion_formal(self):

        tipo_documento = TipoDocumento.objects.create(
            descripcion='LC', longitud=8)
        profesion = Profesion.objects.create(nombre='Mesero')
        sexo = Sexo.objects.create(descripcion='M')

        persona = Persona.objects.create(
            nombre='Alan',
            apellido='Beck',
            tipo_documento=tipo_documento,
            numero_documento='31487249',
            fecha_nacimiento='1985-12-19',
            sexo=sexo,
            profesion=profesion
        )

        empleado_sin_asignacion = Empleado.objects.create(
            persona=persona, fecha_ingreso='1999-01-01',
            fecha_egreso='1999-01-01')

        request = HttpRequest()
        request.method = 'GET'

        request.GET = {
            'empleado': empleado_sin_asignacion.id,
            'asignacion': 10,
            'fecha_desde': '01/01/2010',
        }

        response = helpers.get_validar_fechas_historial_asigancion_formal(
            request)
        result = self.get_dict_from_response(response)

        # EN CASO DE UN ALTA: NO EXISTE FECHA DE HISTORIAL CON QUE COMPARAR
        # DEVUELVE 0
        self.assertEqual(0, result['msj'])

        # PARA MODI
        empleado = self.empleado
        destino = self.institucion

        AsignacionFormal.objects.create(
            empleado=empleado,
            destino=destino,
            fecha_desde='2010-01-01',
            fecha_hasta='2010-12-31',
        )

        AsignacionFormal.objects.create(
            empleado=empleado,
            destino=destino,
            fecha_desde='2011-01-01',
            fecha_hasta='2011-12-31',
        )

        AsignacionFormal.objects.create(
            empleado=empleado,
            destino=destino,
            fecha_desde='2012-01-01',
            fecha_hasta='2012-12-31',
        )

        request = HttpRequest()
        request.method = 'GET'

        request.GET = {
            'empleado': empleado.id,
            'asignacion': 3,
            'fecha_desde': '01/01/2013',
        }

        response = helpers.get_validar_fechas_historial_asigancion_formal(
            request)
        result = self.get_dict_from_response(response)

        # EN CASO DE UN MODI - CON FECHA DESDE MENOR NI IGUAL A
        # NINGUNO DEL HISTORIAL - DEVUELVE 0
        self.assertEqual(0, result['msj'])

        request.GET = {
            'empleado': empleado.id,
            'asignacion': 3,
            'fecha_desde': '01/10/2011',
        }

        response = helpers.get_validar_fechas_historial_asigancion_formal(
            request)
        result = self.get_dict_from_response(response)

        # EN CASO DE UN MODI - CON FECHA DESDE MENOR NI IGUAL A
        # ALGUNO DEL HISTORIAL - DEVUELVE 1
        self.assertEqual(1, result['msj'])

    def get_dict_from_response(self, response):
        data_string = response.content.decode("utf-8")
        result = ast.literal_eval(data_string)

        return result

    def get_pais_object(self):
        pais = Pais.objects.create(nombre='ARG')

        return pais

    def get_provincia_object(self):
        pais = self.get_pais_object()
        provincia = Provincia.objects.create(
            nombre='Formosa',
            pais=pais
        )

        return provincia

    def get_departamento_object(self):
        provincia = self.get_provincia_object()
        departamento = Departamento.objects.create(
            nombre='FSA',
            provincia=provincia
        )

        return departamento

    def get_institucion_object(self):

        pais = self.get_pais_object()
        provincia = self.get_provincia_object()
        departamento = self.get_departamento_object()

        institucion = Institucion.objects.create(
            nombre='HAC',
            cuit='23301548967',
            telefono='4423568',
            pais=pais,
            provincia=provincia,
            departamento=departamento,
            domicilio='Av Americas y P Gomez'
        )

        return institucion

    def get_sexo_object(self):
        sexo = Sexo.objects.create(descripcion='Masculino')

        return sexo

    def get_tipo_documento_object(self):
        tipo_documento = TipoDocumento.objects.create(
            descripcion='DNI', longitud=8)

        return tipo_documento

    def get_profesion_object(self):
        profesion = Profesion.objects.create(nombre='Programador')

        return profesion

    def get_empleado_object(self):

        tipo_documento = self.get_tipo_documento_object()
        profesion = self.get_profesion_object()
        sexo = self.get_sexo_object()

        persona = Persona.objects.create(
            nombre='Fernando',
            apellido='Riquelme',
            tipo_documento=tipo_documento,
            numero_documento='30194000',
            fecha_nacimiento='1983-06-19',
            sexo=sexo,
            profesion=profesion
        )

        empleado = Empleado.objects.create(
            persona=persona, fecha_ingreso='1999-01-01',
            fecha_egreso='1999-01-01')

        return empleado

    def test_get_datos_para_select_asignacion_formal(self):

        institucion = self.institucion

        request = HttpRequest()
        request.method = 'GET'

        request.GET = {
            'id': institucion.id,
            'tabla': "institucion"
        }

        response = helpers.get_datos_para_select_asignacion_formal(request)
        result = self.get_dict_from_response(response)

        # CUANDO NO TIENE CARGOS ASOCIADOS EL DESTINO-INSTITUCION
        self.assertEqual(1, len(result['cargos']))

        # CUANDO NO TIENE DIRECCIONES ASOCIADOS EL DESTINO-INSTITUCION
        self.assertEqual(1, len(result['direcciones']))

        Cargo.objects.create(
            institucion=institucion,
            descripcion='JEFE_HAC'
        )

        Cargo.objects.create(
            institucion=institucion,
            descripcion='SUB_JEFE_HAC'
        )

        Direccion.objects.create(
            institucion=institucion,
            descripcion='RESP_DIRECCION_HAC'
        )

        Direccion.objects.create(
            institucion=institucion,
            descripcion='SUB_RESPONSABLE_DIRECCION_HAC'
        )

        request.GET = {
            'id': institucion.id,
            'tabla': "institucion"
        }

        response = helpers.get_datos_para_select_asignacion_formal(request)
        result = self.get_dict_from_response(response)

        # CUANDO TIENE 2 CARGOS ASOCIADOS EL DESTINO-INSTITUCION
        self.assertEqual(3, len(result['cargos']))

        # CUANDO TIENE 2 DIRECCIONES ASOCIADOS EL DESTINO-INSTITUCION
        self.assertEqual(3, len(result['direcciones']))

        request = HttpRequest()
        request.method = 'GET'

        direccion = Direccion.objects.get(pk=1)

        request.GET = {
            'id': direccion.id,
            'tabla': "departamento"
        }

        response = helpers.get_datos_para_select_asignacion_formal(request)
        result = self.get_dict_from_response(response)

        # CUANDO NO TIENE DEPARTAMENTOS ASOCIADOS LA DIRECCION
        self.assertEqual(1, len(result['query']))

        DepartamentoAsignacion.objects.create(
            direccion=direccion,
            descripcion='INFORMATICA'
        )

        response = helpers.get_datos_para_select_asignacion_formal(request)
        result = self.get_dict_from_response(response)

        # CUANDO TIENE 1 DEPARTAMENTOS ASOCIADOS LA DIRECCION
        self.assertEqual(2, len(result['query']))