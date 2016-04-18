
import ast
import time

from django.http import HttpRequest
from django.test import TestCase

from apps.empleados.models import Empleado
from apps.expedientes import helpers
from apps.expedientes.models import (Estado, Etapa, NumeroAutoincremental,
                                     Clase, Expediente)
from apps.personas.models import Persona


class HelpersTestCase(TestCase):

    def crear_numeros_autoincrementales(self):
        NumeroAutoincremental.objects.create(numero=0,
                                             tipo='RESOLUCION_ADJUDICACION')
        NumeroAutoincremental.objects.create(numero=0,
                                             tipo='CONTRATACION_DIRECTA')
        NumeroAutoincremental.objects.create(numero=0, tipo='COMPRA_DIRECTA')
        NumeroAutoincremental.objects.create(numero=0, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=10, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=1, tipo='RESOLUCION_PAGO')
        NumeroAutoincremental.objects.create(numero=0, tipo='NUMERO_LICITACION')
        NumeroAutoincremental.objects.create(
            numero=0, tipo='NUMERO_DISPOSICION')

    def test_get_numero_autoincremental(self):

        self.crear_numeros_autoincrementales()

        numero = helpers.get_numero_autoincremental('RESOLUCION_ADJUDICACION')
        self.assertEqual(1, numero)

        numero = helpers.get_numero_autoincremental('ORDEN_PROVISION')
        self.assertEqual(11, numero)

    def test_guardar_numero_autoincremental(self):

        self.crear_numeros_autoincrementales()

        helpers.guardar_numero_autoincremental('RESOLUCION_ADJUDICACION', 1)
        numero = helpers.get_numero_autoincremental('RESOLUCION_ADJUDICACION')

        self.assertEqual(2, numero)

        numero = helpers.get_numero_autoincremental('ORDEN_PROVISION')
        helpers.guardar_numero_autoincremental('ORDEN_PROVISION', numero)
        numero = helpers.get_numero_autoincremental('ORDEN_PROVISION')

        self.assertEqual(12, numero)

    def test_registrar_numeros_autoincrementales(self):

        self.crear_numeros_autoincrementales()

        listado = {
            'RESOLUCION_ADJUDICACION': 1,
            'ORDEN_PROVISION': 11,
            'ACTA_RECEPCION': 1
            }

        helpers.registrar_numeros_autoincrementales(listado)

        numero = helpers.get_numero_autoincremental('RESOLUCION_ADJUDICACION')
        self.assertEqual(2, numero)

        numero = helpers.get_numero_autoincremental('ORDEN_PROVISION')
        self.assertEqual(12, numero)

        numero = helpers.get_numero_autoincremental('ACTA_RECEPCION')
        self.assertEqual(2, numero)

    def test_numero_es_valido(self):

        self.crear_numeros_autoincrementales()

        es_valido = helpers.numero_es_valido('ORDEN_PROVISION', 15)
        self.assertFalse(es_valido)

        es_valido = helpers.numero_es_valido('ORDEN_PROVISION', 10)
        self.assertTrue(es_valido)

        es_valido = helpers.numero_es_valido('ORDEN_PROVISION', 8)
        self.assertTrue(es_valido)

    def test_get_etapa(self):

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'etapa_id': 10}

        response = helpers.get_etapa(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(0, len(result))

        request.GET = {'etapa_id': 1}

        response = helpers.get_etapa(request)
        result = self.get_dict_from_response(response)

        self.assertGreater(len(result), 0)
        self.assertIn('etapa_id', result)
        self.assertIn('valor', result)
        self.assertEqual('PREVENTIVO', result['valor'])

    def test_get_estado_valor(self):

        Estado.objects.create(descripcion='reservado', valor='RESERVADO')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
        Estado.objects.create(descripcion='cerrado', valor='CERRADO')

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'estado_id': 1}

        response = helpers.get_estado_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('RESERVADO', result)

        request.GET = {'estado_id': 3}

        response = helpers.get_estado_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('CERRADO', result)

        request.GET = {'estado_id': 111}

        response = helpers.get_estado_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(0, len(result))

    def test_get_valores_compra_directa(self):

        self.crear_numeros_autoincrementales()

        result = helpers.get_valores_compra_directa()

        self.assertIn('result', result)
        self.assertIn('tipo_transaccion', result)
        self.assertIn('numero_identificacion_transaccion', result)
        self.assertEqual('COMPRA DIRECTA', result['tipo_transaccion'])

    def test_get_valores_contratacion_directa(self):

        self.crear_numeros_autoincrementales()

        result = helpers.get_valores_contratacion_directa()

        self.assertIn('result', result)
        self.assertIn('tipo_transaccion', result)
        self.assertIn('numero_identificacion_transaccion', result)
        self.assertEqual('CONTRATACION DIRECTA', result['tipo_transaccion'])

    def test_get_tipo_transaccion(self):

        self.crear_numeros_autoincrementales()

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'importe': 1000}

        response = helpers.get_tipo_transaccion(request)
        tipo_transaccion = self.get_dict_from_response(response)

        self.assertIn('result', tipo_transaccion)
        self.assertEqual('error', tipo_transaccion['result'])

        request.GET = {'importe': 1199}

        response = helpers.get_tipo_transaccion(request)
        tipo_transaccion = self.get_dict_from_response(response)

        self.assertIn('result', tipo_transaccion)
        self.assertEqual('error', tipo_transaccion['result'])

        request.GET = {'importe': 1200}

        response = helpers.get_tipo_transaccion(request)
        tipo_transaccion = self.get_dict_from_response(response)

        self.assertIn('result', tipo_transaccion)
        self.assertIn('tipo_transaccion', tipo_transaccion)
        self.assertIn('numero_identificacion_transaccion', tipo_transaccion)

        self.assertEqual('ok', tipo_transaccion['result'])
        self.assertEqual('COMPRA DIRECTA', tipo_transaccion['tipo_transaccion'])
        self.assertEqual(
            1, tipo_transaccion['numero_identificacion_transaccion'])

        # request.GET = {'importe': 12001} # POR CAMBIO EN HELPER DE LOS MONTOS
        request.GET = {'importe': 12501}

        response = helpers.get_tipo_transaccion(request)
        tipo_transaccion = self.get_dict_from_response(response)

        self.assertIn('result', tipo_transaccion)
        self.assertIn('tipo_transaccion', tipo_transaccion)
        self.assertIn('numero_identificacion_transaccion', tipo_transaccion)

        self.assertEqual('ok', tipo_transaccion['result'])
        self.assertEqual(
            'CONTRATACION DIRECTA', tipo_transaccion['tipo_transaccion'])
        self.assertEqual(
            1, tipo_transaccion['numero_identificacion_transaccion'])

    def test_get_numero_ingreso_manual_es_valido(self):

        self.crear_numeros_autoincrementales()

        request = HttpRequest()
        request.method = 'GET'

        request.GET = {
            'tipo': "ORDEN_PROVISION",
            'numero': 25
        }

        response = helpers.get_numero_ingreso_manual_es_valido(request)
        es_valido = self.get_dict_from_response_dato_ingreso_manual(response)

        self.assertFalse(es_valido)

        request.GET = {
            'tipo': 'ORDEN_PROVISION',
            'numero': 10
        }

        response = helpers.get_numero_ingreso_manual_es_valido(request)
        es_valido = self.get_dict_from_response_dato_ingreso_manual(response)

        self.assertTrue(es_valido)

    def test_get_fecha_resolucion_pago_es_valido(self):

        request = HttpRequest()
        request.method = 'GET'

        request.GET = {
            'fecha': "as/11/2015"
        }

        response = helpers.get_fecha_resolucion_pago_es_valido(request)
        es_valido = self.get_dict_from_response_dato_ingreso_manual(response)

        self.assertFalse(es_valido)

        request.GET = {
            'fecha': "16/11/2015"
        }

        response = helpers.get_fecha_resolucion_pago_es_valido(request)
        es_valido = self.get_dict_from_response_dato_ingreso_manual(response)

        # self.assertTrue(es_valido)  # CONTROLAR CON DIEGO
        self.assertFalse(es_valido)

    def test_get_clase_valor(self):

        Clase.objects.create(descripcion='disposicion', valor='DISPOSICION')
        Clase.objects.create(descripcion='resolucion', valor='RESOLUCION')
        Clase.objects.create(descripcion='servicios', valor='SERVICIOS')

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'clase_id': 1}

        response = helpers.get_clase_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('DISPOSICION', result['valor'])

        request.GET = {'clase_id': 3}

        response = helpers.get_clase_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('SERVICIOS', result['valor'])

        request.GET = {'clase_id': 111}

        response = helpers.get_clase_valor(request)
        result = self.get_dict_from_response(response)

        self.assertEqual(0, len(result))

    def test_get_numero_autoincremental_ajax(self):

        self.crear_numeros_autoincrementales()

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'tipo': "ORDEN_PROVISION"}

        response = helpers.get_numero_autoincremental_ajax(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('0011', result['numero'])

        request.GET = {'tipo': "RESOLUCION_ADJUDICACION"}

        response = helpers.get_numero_autoincremental_ajax(request)
        result = self.get_dict_from_response(response)

        self.assertEqual('0001', result['numero'])

    def get_dict_from_response(self, response):
        data_string = response.content.decode("utf-8")
        tipo_transaccion = ast.literal_eval(data_string)

        return tipo_transaccion

    def get_dict_from_response_dato_ingreso_manual(self, response):
        data_string = response.content.decode("utf-8")
        result = ast.literal_eval(data_string.title())

        return result

    def test_get_expedientes_con_reserva_mayor_15_dias(self):

        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)

        clase = Clase.objects.create(
            descripcion='resolucion', valor='RESOLUCION')

        estado = Estado.objects.create(
            descripcion='reservado', valor='RESERVADO')

        Expediente.objects.create(
            letra='H',
            numero=1,
            anio=2015,
            clase=clase,
            estado=estado,
            fecha='2016-03-01',
            # fecha='2016-04-01',  # FECHA ACTUAL
            empleado_solicitante=empleado
        )

        request = HttpRequest()
        request.method = 'GET'
        request.GET = {}

        response = helpers.get_expedientes_con_reserva_mayor_15_dias(request)
        result = self.get_dict_from_response_reserva_expediente(response)

        self.assertEqual(1, result)

        # self.assertEqual(0, result) # SI CAMBIAMOS LA FECHA A LA ACTUAL

    def test_generar_numero_expediente(self):

        expedientes = Expediente.objects.all()
        self.assertEqual(0, len(expedientes))

        result = helpers.generar_numero_expediente()
        self.assertEqual(1, int(result))

        anio_actual = time.strftime("%y")

        clase = Clase.objects.create(
            descripcion='Resoluciones Varias', valor='RESOLUCIONES_VARIAS')
        Expediente.objects.create(
            letra='H', numero=1, anio=anio_actual, clase=clase)
        Expediente.objects.create(
            letra='A', numero=1, anio=anio_actual, clase=clase)

        result = helpers.generar_numero_expediente()
        self.assertEqual(2, int(result))

    def get_dict_from_response_reserva_expediente(self, response):
        data_string = response.content.decode("utf-8")
        result = ast.literal_eval(data_string)

        return result