# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.empleados.models import Empleado
from apps.personas.models import Persona

from apps.expedientes.models import (Expediente, ExpedienteResolucion, Estado,
                                     Clase, Etapa, FuenteFinanciamiento,
                                     NumeroAutoincremental,
                                     ExpedienteServicioMedico,
                                     ExpedienteLicitacion,
                                     ExpedienteResolucionesVarias,
                                     TipoResolucion,
                                     ExpedienteResolucionContratacion)

from apps.expedientes.views import (ExpedienteUpdate, ExpedienteListView,
                                    ExpedienteResolucionCreate,
                                    ExpedienteResolucionUpdate,
                                    ExpedienteServicioMedicoCreate,
                                    ExpedienteLicitacionCreate,
                                    ExpedienteLicitacionUpdate,
                                    ExpedienteComodatoCreate,
                                    ExpedienteResolucionesVariasCreate,
                                    ExpedienteResolucionContratacionCreate)

from apps.proveedores.models import Proveedor


# --------------------------------------------------------
# TEST Expediente
# --------------------------------------------------------


class ExpedienteUpdateTestCase(TestCase):

    def test_tiene_clase_creada(self):

        expediente_update = ExpedienteUpdate()

        clase = Clase.objects.create(
            descripcion='Resolucion', valor='RESOLUCION')
        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015, clase=clase)

        tiene_clase_creada = expediente_update.tiene_clase_creada(expediente)

        self.assertFalse(tiene_clase_creada)

        ExpedienteResolucion.objects.create(
            expediente=expediente,
            resolucion_adjudicacion=1
        )

        tiene_clase_creada = expediente_update.tiene_clase_creada(expediente)

        self.assertTrue(tiene_clase_creada)


class ExpedienteListViewTestCase(TestCase):

    def setUp(self):

        persona = Persona.objects.create(apellido='perez', nombre='juan')

        empleado = Empleado.objects.create(persona=persona)

        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        tipo_resolucion = TipoResolucion.objects.create(
            descripcion='Legales', valor='LEGALES')

        clase = Clase.objects.create(
            descripcion='Resolucion', valor='RESOLUCION')

        estado = Estado.objects.create(
            descripcion='pendiente', valor='PENDIENTE')

        estado_reservado = Estado.objects.create(
            descripcion='reservado', valor='RESERVADO')

        Expediente.objects.create(
            letra='H',
            numero=1,
            anio=2015,
            clase=clase,
            fecha='2015-09-01',
            empleado_solicitante=empleado,
            tipo_resolucion=tipo_resolucion

        )

        Expediente.objects.create(
            letra='A',
            numero=1,
            anio=2015,
            clase=clase,
            fecha='2015-09-11',
            estado=estado,
            empleado_solicitante=empleado,
            tipo_resolucion=tipo_resolucion
        )

        Expediente.objects.create(
            letra='A',
            numero=3,
            anio=2015,
            clase=clase,
            fecha='2015-09-11',
            estado=estado_reservado,
            empleado_solicitante=empleado,
            tipo_resolucion=tipo_resolucion
        )

        expediente1 = Expediente.objects.get(pk=1)
        expediente2 = Expediente.objects.get(pk=2)

        ExpedienteResolucion.objects.create(
            expediente=expediente1,
            resolucion_adjudicacion=1,
            fecha_resolucion_pago='2015-09-01',
        )

        ExpedienteServicioMedico.objects.create(
            expediente=expediente2,
            profesional=empleado,
            resolucion_contratacion='AXZY001',
            fecha_resolucion_contratacion='2015-11-01',
            orden_provision=1,
            acta_recepcion=1,
            numero_resolucion_pago=1,
            fecha_resolucion_pago='2015-11-01',
            importe=100,
            solicitante_resolucion_pago=empleado,
            fuente_financiamiento=fuente_financiamiento
        )

    def tearDown(self):

        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()
        ExpedienteResolucion.objects.all().delete()
        ExpedienteServicioMedico.objects.all().delete()
        Clase.objects.all().delete()

    def test_buscar_por_numero_expediente(self):

        expediente_listview = ExpedienteListView()

        result = expediente_listview.buscar_por_numero('2', '14')
        self.assertEqual(0, len(result))

        result = expediente_listview.buscar_por_numero('1', '15')
        self.assertEqual(2, len(result))

    def test_buscar_por_numero_resolucion_pago(self):

        expediente_listview = ExpedienteListView()

        result = \
            expediente_listview.buscar_por_numero_resolucion_pago('2')
        self.assertEqual(0, len(result))

        result =\
            expediente_listview.buscar_por_numero_resolucion_pago('1')
        self.assertEqual(1, len(result))

    def test_buscar_por_fecha_expediente(self):

        expediente_listview = ExpedienteListView()

        result =\
            expediente_listview.buscar_por_fecha_expediente(
                '02/09/2015', '07/09/2015')
        self.assertEqual(0, len(result))

        result =\
            expediente_listview.buscar_por_fecha_expediente(
                '01/09/2015', '07/09/2015')
        self.assertEqual(1, len(result))

        result =\
            expediente_listview.buscar_por_fecha_expediente(
                '01/09/2015', '')
        # self.assertEqual(2, len(result))
        self.assertEqual(3, len(result))

    def test_buscar_por_fecha_resolucion_pago(self):

        expediente_listview = ExpedienteListView()

        result = expediente_listview.buscar_por_fecha_resolucion_pago(
            '02/09/2015', '07/09/2015')
        self.assertEqual(0, len(result))

        result = expediente_listview.buscar_por_fecha_resolucion_pago(
            '01/09/2015', '12/11/2015')
        self.assertEqual(2, len(result))

    def test_buscar_por_estado_expediente(self):

        expediente_listview = ExpedienteListView()

        result = expediente_listview.buscar_por_estado('x')
        self.assertEqual(0, len(result))

        result = expediente_listview.buscar_por_estado('PENDIENTE')
        self.assertEqual(1, len(result))

    def test_buscar_por_empleado_solicitante(self):

        expediente_listview = ExpedienteListView()

        result = expediente_listview.buscar_por_empleado_solicitante('99')
        self.assertEqual(0, len(result))

        result = expediente_listview.buscar_por_empleado_solicitante('1')
        # self.assertEqual(2, len(result))
        self.assertEqual(3, len(result))

    def test_buscar_por_tipo_resolucion(self):

        sut = ExpedienteListView()

        result = sut.buscar_por_tipo_resolucion('CONTRATACIONES')
        self.assertEqual(0, len(result))

        result = sut.buscar_por_tipo_resolucion('LEGALES')
        # self.assertEqual(2, len(result))
        self.assertEqual(3, len(result))

    def test_buscar_por_reserva_mayor_15_dias(self):

        sut = ExpedienteListView()

        result = sut.buscar_por_reserva_mayor_15_dias('0')
        self.assertEqual(1, len(result))

        result = sut.buscar_por_reserva_mayor_15_dias('1')
        self.assertEqual(1, len(result))


# --------------------------------------------------------
# TEST Expediente Resolucion
# --------------------------------------------------------


class ExpedienteResolucionCreateTestCase(TestCase):

    def setUp(self):
        self.sut = ExpedienteResolucionCreate()

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='Resolucion', valor='RESOLUCION')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(descripcion='compromiso', valor='COMPROMISO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def test_actualizar_etapa_estado_expediente(self):

        expediente = self.get_expediente_object()

        self.assertEqual('PREVENTIVO', expediente.etapa.valor)
        self.assertEqual('RESERVADO', expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(2, expediente)

        self.assertEqual('COMPROMISO', expediente.etapa.valor)
        self.assertEqual('PENDIENTE', expediente.estado.valor)

    def test_get_tipo_transaccion(self):

        result = self.sut.get_tipo_transaccion(500)
        self.assertEqual('COMPRA_DIRECTA', result)

        # result = self.sut.get_tipo_transaccion(12001)
        result = self.sut.get_tipo_transaccion(12501)
        self.assertEqual('CONTRATACION_DIRECTA', result)

    def test_guardar_numeros_autoincrementales(self):

        NumeroAutoincremental.objects.create(
            numero=2, tipo='RESOLUCION_PAGO')
        NumeroAutoincremental.objects.create(numero=3, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=3, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=5, tipo='COMPRA_DIRECTA')
        NumeroAutoincremental.objects.create(numero=10,
                                             tipo='CONTRATACION_DIRECTA')

        expediente = self.get_expediente_object()

        expediente_resolucion = ExpedienteResolucion.objects.create(
            expediente=expediente,
            resolucion_adjudicacion=3,
            orden_provision=4,
            acta_recepcion=2,
            importe=500,
            numero_identificacion_transaccion=6
        )

        self.sut.guardar_numeros_autoincrementales(expediente_resolucion)

        resolucion_adjudicacion = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')
        orden_provision = NumeroAutoincremental.objects.get(
            tipo='ORDEN_PROVISION')
        acta_recepcion = NumeroAutoincremental.objects.get(
            tipo='ACTA_RECEPCION')
        compra_directa = NumeroAutoincremental.objects.get(
            tipo='COMPRA_DIRECTA')
        contratacion_directa = NumeroAutoincremental.objects.get(
            tipo='CONTRATACION_DIRECTA')

        self.assertEqual(3, resolucion_adjudicacion.numero)
        self.assertEqual(4, orden_provision.numero)
        self.assertEqual(3, acta_recepcion.numero)
        self.assertEqual(6, compra_directa.numero)
        self.assertEqual(10, contratacion_directa.numero)

        expediente_resolucion.importe = 15000
        expediente_resolucion.numero_identificacion_transaccion = 11

        self.sut.guardar_numeros_autoincrementales(expediente_resolucion)

        resolucion_adjudicacion = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')
        orden_provision = NumeroAutoincremental.objects.get(
            tipo='ORDEN_PROVISION')
        acta_recepcion = NumeroAutoincremental.objects.get(
            tipo='ACTA_RECEPCION')
        compra_directa = NumeroAutoincremental.objects.get(
            tipo='COMPRA_DIRECTA')
        contratacion_directa = NumeroAutoincremental.objects.get(
            tipo='CONTRATACION_DIRECTA')

        self.assertEqual(3, resolucion_adjudicacion.numero)
        self.assertEqual(4, orden_provision.numero)
        self.assertEqual(3, acta_recepcion.numero)
        self.assertEqual(6, compra_directa.numero)
        self.assertEqual(11, contratacion_directa.numero)

    def test_get_numeros_autoincrementales(self):

        NumeroAutoincremental.objects.create(numero=15, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=3, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=7, tipo='RESOLUCION_PAGO')

        resolucion_adjudicacion, orden_provision, acta_recepcion = (
            None, None, None)

        listado = self.sut.get_numeros_autoincrementales(
            resolucion_adjudicacion, orden_provision, acta_recepcion)

        self.assertEqual(16, listado['orden_provision'])
        self.assertEqual(4, listado['acta_recepcion'])
        self.assertEqual(8, listado['resolucion_adjudicacion'])

        resolucion_adjudicacion, orden_provision, acta_recepcion = None, 5, None

        listado = self.sut.get_numeros_autoincrementales(
            resolucion_adjudicacion, orden_provision, acta_recepcion)

        self.assertEqual(5, listado['orden_provision'])
        self.assertEqual(4, listado['acta_recepcion'])
        self.assertEqual(8, listado['resolucion_adjudicacion'])

        resolucion_adjudicacion, orden_provision, acta_recepcion = 4, 12, 1

        listado = self.sut.get_numeros_autoincrementales(
            resolucion_adjudicacion, orden_provision, acta_recepcion)

        self.assertEqual(12, listado['orden_provision'])
        self.assertEqual(1, listado['acta_recepcion'])
        self.assertEqual(4, listado['resolucion_adjudicacion'])


class ExpedienteResolucionUpdateTestCase(TestCase):

    def setUp(self):
        # SUT = Subject Under Test
        # Se usa abreviatura que se refiere a expediente_resolucion_update
        self.sut = ExpedienteResolucionUpdate()

        clase = Clase.objects.create(
            descripcion='Resolucion', valor='RESOLUCION')

        self.expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015, clase=clase)

    def tearDown(self):
        Clase.objects.all().delete()
        Expediente.objects.all().delete()

    def test_get_puede_actualizar_numeros(self):

        expediente_resolucion = ExpedienteResolucion.objects.create(
            expediente=self.expediente,
            resolucion_adjudicacion=3,
            orden_provision=0,
            acta_recepcion=0,
            numero_resolucion_pago=1
        )

        result = self.sut.get_puede_actualizar_numeros(expediente_resolucion)

        self.assertFalse(result[0])
        self.assertTrue(result[1])

        expediente_resolucion.orden_provision = 1
        expediente_resolucion.acta_recepcion = 1
        expediente_resolucion.numero_resolucion_pago = 0

        result = self.sut.get_puede_actualizar_numeros(expediente_resolucion)

        self.assertTrue(result[0])
        self.assertFalse(result[1])

        expediente_resolucion.orden_provision = 1
        expediente_resolucion.acta_recepcion = 1
        expediente_resolucion.numero_resolucion_pago = 1

        result = self.sut.get_puede_actualizar_numeros(expediente_resolucion)

        self.assertTrue(result[0])
        self.assertTrue(result[1])

        expediente_resolucion.orden_provision = 1
        expediente_resolucion.acta_recepcion = 0
        expediente_resolucion.numero_resolucion_pago = 1

        result = self.sut.get_puede_actualizar_numeros(expediente_resolucion)

        self.assertFalse(result[0])
        self.assertTrue(result[1])

    def test_actualizar_etapa_estado_expediente(self):

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(descripcion='compromiso', valor='COMPROMISO')
        Etapa.objects.create(descripcion='ordenado', valor='ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='disponible', valor='DISPONIBLE')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
        Estado.objects.create(descripcion='cerrado', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        self.expediente.estado = estado
        self.expediente.etapa = etapa
        self.expediente.save()

        self.assertEqual('RESERVADO', self.expediente.estado.valor)
        self.assertEqual('PREVENTIVO', self.expediente.etapa.valor)

        self.sut.actualizar_etapa_estado_expediente(2, self.expediente)

        self.assertEqual('PENDIENTE', self.expediente.estado.valor)
        self.assertEqual('COMPROMISO', self.expediente.etapa.valor)

        self.sut.actualizar_etapa_estado_expediente(3, self.expediente)

        self.assertEqual('CERRADO', self.expediente.estado.valor)
        self.assertEqual('ORDENADO', self.expediente.etapa.valor)


# --------------------------------------------------------
# TEST Expediente Servicio Medico
# --------------------------------------------------------


class ExpedienteServicioMedicoCreateTestCase(TestCase):

    def setUp(self):
        self.sut = ExpedienteServicioMedicoCreate()

    def tearDown(self):
        del self.sut

    def test_actualizar_etapa_estado_expediente(self):

        expediente = self.get_expediente_object()

        self.assertEqual('PREVENTIVO', expediente.etapa.valor)
        self.assertEqual('RESERVADO', expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(3, expediente)

        self.assertEqual('ORDENADO', expediente.etapa.valor)
        self.assertNotEqual('CERRADO', expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(4, expediente)

        self.assertEqual('COMPROMISO_ORDENADO', expediente.etapa.valor)
        self.assertEqual('CERRADO', expediente.estado.valor)

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='Resolucion', valor='RESOLUCION')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(descripcion='compromiso', valor='COMPROMISO')
        Etapa.objects.create(descripcion='ordenado', valor='ORDENADO')
        Etapa.objects.create(
            descripcion='compromiso y ordenado', valor='COMPROMISO_ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='disponible', valor='DISPONIBLE')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
        Estado.objects.create(descripcion='cerrado', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def test_get_numeros_autoincrementales(self):

        NumeroAutoincremental.objects.create(numero=15, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=3, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=4, tipo='RESOLUCION_PAGO')

        orden_provision, acta_recepcion, resolucion_pago = None, None, None

        listado = self.sut.get_numeros_autoincrementales(
            orden_provision, acta_recepcion, resolucion_pago)

        self.assertEqual(16, listado['orden_provision'])
        self.assertEqual(4, listado['acta_recepcion'])
        self.assertEqual(5, listado['resolucion_pago'])

        orden_provision, acta_recepcion, resolucion_pago = 5, None, None

        listado = self.sut.get_numeros_autoincrementales(
            orden_provision, acta_recepcion, resolucion_pago)

        self.assertEqual(5, listado['orden_provision'])
        self.assertEqual(4, listado['acta_recepcion'])
        self.assertEqual(5, listado['resolucion_pago'])

        orden_provision, acta_recepcion, resolucion_pago = 12, 1, 2

        listado = self.sut.get_numeros_autoincrementales(
            orden_provision, acta_recepcion, resolucion_pago)

        self.assertEqual(12, listado['orden_provision'])
        self.assertEqual(1, listado['acta_recepcion'])
        self.assertEqual(2, listado['resolucion_pago'])


# --------------------------------------------------------
# TEST Expediente Licitacion - Etapa: Compromiso
# --------------------------------------------------------


class ExpedienteLicitacionCreateTestCase(TestCase):

    def setUp(self):
        # SUT = Subject Under Test
        # Se usa abreviatura que se refiere a expediente_licitacion_create
        self.sut = ExpedienteLicitacionCreate()

        self.expediente = self.get_expediente_object()
        self.expediente_licitacion = self.get_expediente_licitacion_object()

        NumeroAutoincremental.objects.create(
            numero=1, tipo='NUMERO_DISPOSICION')
        NumeroAutoincremental.objects.create(
            numero=1, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=1, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=1, tipo='NUMERO_LICITACION')
        NumeroAutoincremental.objects.create(numero=1, tipo='RESOLUCION_PAGO')

        Proveedor.objects.create(razon_social='SANTA ROSA')
        Proveedor.objects.create(razon_social='CACERES')

    def tearDown(self):
        Clase.objects.all().delete()
        Expediente.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()
        Proveedor.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()

    def test_actualizar_etapa_estado_expediente(self):

        self.assertEqual('PREVENTIVO', self.expediente.etapa.valor)
        self.assertEqual('RESERVADO', self.expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(2, self.expediente)

        self.assertEqual('COMPROMISO', self.expediente.etapa.valor)
        self.assertEqual('PENDIENTE', self.expediente.estado.valor)
        self.assertNotEqual('CERRADO', self.expediente.estado.valor)

    def test_guardar_items_compromiso(self):

        datos = [
            {
                'proveedor': 'SANTA ROSA',
                'orden_provision': '',
                'monto_total': '6363',
                'monto': '6363'
            },
            {
                'proveedor': 'CACERES',
                'orden_provision': '',
                'monto_total': '6969',
                'monto': '6969'
            }
        ]

        self.sut.guardar_items_compromiso(datos, self.expediente_licitacion)

        items_compromiso = \
            self.expediente_licitacion.expedientelicitacioncompromiso_set.all()

        self.assertNotEqual(1, len(items_compromiso))
        self.assertEqual(2, len(items_compromiso))

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='licitacion', valor='LICITACION')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(descripcion='compromiso', valor='COMPROMISO')
        Etapa.objects.create(descripcion='ordenado', valor='ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='disponible', valor='DISPONIBLE')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
        Estado.objects.create(descripcion='cerrado', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def get_expediente_licitacion_object(self):

        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        expediente_licitacion = ExpedienteLicitacion.objects.create(
            expediente=self.expediente,
            numero=1,
            anio=15,
            numero_disposicion=1,
            resolucion_aprobacion=1,
            fecha_resolucion_aprobacion='2015-11-06',
            resolucion_adjudicacion=22,
            fecha_resolucion_adjudicacion='2015-11-06',
            fuente_financiamiento=fuente_financiamiento
        )

        return expediente_licitacion


class ExpedienteLicitacionUpdateTestCase(TestCase):

    def setUp(self):
        # SUT = Subject Under Test
        # Se usa abreviatura que se refiere a expediente_licitacion_update
        self.sut = ExpedienteLicitacionUpdate()

        self.expediente = self.get_expediente_object()
        self.expediente_licitacion = self.get_expediente_licitacion_object()

        NumeroAutoincremental.objects.create(
            numero=1, tipo='NUMERO_DISPOSICION')
        NumeroAutoincremental.objects.create(
            numero=1, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=1, tipo='ACTA_RECEPCION')
        NumeroAutoincremental.objects.create(numero=1, tipo='NUMERO_LICITACION')
        NumeroAutoincremental.objects.create(numero=1, tipo='RESOLUCION_PAGO')

        Proveedor.objects.create(razon_social='SANTA ROSA')
        Proveedor.objects.create(razon_social='CACERES')

        Persona.objects.create(apellido='perez', nombre='juan')
        persona = Persona.objects.get(pk=1)

        Persona.objects.create(apellido='Escudero', nombre='juan')
        persona2 = Persona.objects.get(pk=2)

        Empleado.objects.create(persona=persona)
        Empleado.objects.create(persona=persona2)

    def tearDown(self):
        Empleado.objects.all().delete()
        Clase.objects.all().delete()
        Expediente.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()
        Proveedor.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()

    def test_actualizar_etapa_estado_expediente(self):

        self.assertEqual('PREVENTIVO', self.expediente.etapa.valor)
        self.assertEqual('RESERVADO', self.expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(2, self.expediente)

        self.assertEqual('COMPROMISO', self.expediente.etapa.valor)
        self.assertEqual('RESERVADO', self.expediente.estado.valor)

        self.sut.actualizar_etapa_estado_expediente(3, self.expediente)

        self.assertEqual('ORDENADO', self.expediente.etapa.valor)
        self.assertNotEqual('RESERVADO', self.expediente.estado.valor)
        self.assertEqual('CERRADO', self.expediente.estado.valor)

    def test_guardar_items_ordenado(self):

        datos = [
            {
                'monto': 2526,
                'solicitante': '2',
                'resolucion_pago': '',
                'monto_total': None,
                'acta_recepcion': '1',
                'orden_provision': '1',
                'fecha_resolucion_pago': '06/11/2015',
                'observaciones': 'ITEMS ORDENADO',
                'proveedor': 'SANTA ROSA'
            },
            {
                'monto': 1515,
                'solicitante': '1',
                'resolucion_pago': '',
                'monto_total': None,
                'acta_recepcion': '1',
                'orden_provision': '1',
                'fecha_resolucion_pago': '06/11/2015',
                'observaciones': 'ITEMS ORDENADO 2',
                'proveedor': 'CACERES'
            }
        ]

        self.sut.guardar_items_ordenado(datos, self.expediente_licitacion)

        items_ordenado = \
            self.expediente_licitacion.expedientelicitacionordenado_set.all()

        self.assertNotEqual(1, len(items_ordenado))
        self.assertEqual(2, len(items_ordenado))

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='licitacion', valor='LICITACION')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(descripcion='compromiso', valor='COMPROMISO')
        Etapa.objects.create(descripcion='ordenado', valor='ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='disponible', valor='DISPONIBLE')
        Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
        Estado.objects.create(descripcion='cerrado', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def get_expediente_licitacion_object(self):

        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        expediente_licitacion = ExpedienteLicitacion.objects.create(
            expediente=self.expediente,
            numero=1,
            anio=15,
            numero_disposicion=1,
            resolucion_aprobacion=1,
            fecha_resolucion_aprobacion='2015-11-06',
            resolucion_adjudicacion=22,
            fecha_resolucion_adjudicacion='2015-11-06',
            fuente_financiamiento=fuente_financiamiento
        )

        return expediente_licitacion


class ExpedienteComodatoCreateTest(TestCase):

        def setUp(self):
            self.sut = ExpedienteComodatoCreate()
            self.expediente = self.get_expediente_object()

        def tearDown(self):
            Clase.objects.all().delete()
            Expediente.objects.all().delete()

        def get_expediente_object(self):

            clase = Clase.objects.create(
                descripcion='comodato', valor='COMODATO')

            Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
            Etapa.objects.create(
                descripcion='compromiso y ordenado',
                valor='COMPROMISO_ORDENADO'
                )

            Estado.objects.create(descripcion='reserva', valor='RESERVADO')
            Estado.objects.create(descripcion='disponible', valor='DISPONIBLE')
            Estado.objects.create(descripcion='pendiente', valor='PENDIENTE')
            Estado.objects.create(descripcion='cerrado', valor='CERRADO')

            etapa = Etapa.objects.get(pk=1)
            estado = Estado.objects.get(pk=1)

            expediente = Expediente.objects.create(
                letra='H', numero=1, anio=2015,
                clase=clase, estado=estado, etapa=etapa)

            return expediente


class ExpedienteResolucionesVariasCreateTestCase(TestCase):

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='Resoluciones varias', valor='RESOLUCIONES_VARIAS')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(
            descripcion='compromiso', valor='COMPROMISO_ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='pendiente', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def test_actualizar_etapa_estado_expediente(self):

        sut = ExpedienteResolucionesVariasCreate()

        expediente = self.get_expediente_object()

        self.assertEqual('PREVENTIVO', expediente.etapa.valor)
        self.assertEqual('RESERVADO', expediente.estado.valor)

        sut.actualizar_etapa_estado_expediente(2, expediente)

        self.assertEqual('COMPROMISO_ORDENADO', expediente.etapa.valor)
        self.assertEqual('CERRADO', expediente.estado.valor)

    def test_guardar_numeros_autoincrementales(self):

        NumeroAutoincremental.objects.create(numero=2, tipo='RESOLUCION_PAGO')

        expediente = self.get_expediente_object()

        expediente_resoluciones = ExpedienteResolucionesVarias.objects.create(
            expediente=expediente, resolucion_pago=3)

        sut = ExpedienteResolucionesVariasCreate()
        sut.guardar_numeros_autoincrementales(expediente_resoluciones)

        resolucion_pago = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(3, resolucion_pago.numero)

        expediente_resoluciones.resolucion_pago = 10

        sut.guardar_numeros_autoincrementales(expediente_resoluciones)

        resolucion_pago = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(10, resolucion_pago.numero)

        expediente_resoluciones.resolucion_pago = 5

        sut.guardar_numeros_autoincrementales(expediente_resoluciones)

        resolucion_pago = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(10, resolucion_pago.numero)


class ExpedienteResolucionContratacionCreateTestCase(TestCase):

    def get_expediente_object(self):

        clase = Clase.objects.create(
            descripcion='resolucion contratacion',
            valor='RESOLUCION_CONTRATACION')

        Etapa.objects.create(descripcion='preventivo', valor='PREVENTIVO')
        Etapa.objects.create(
            descripcion='compromiso', valor='COMPROMISO_ORDENADO')

        Estado.objects.create(descripcion='reserva', valor='RESERVADO')
        Estado.objects.create(descripcion='pendiente', valor='CERRADO')

        etapa = Etapa.objects.get(pk=1)
        estado = Estado.objects.get(pk=1)

        expediente = Expediente.objects.create(
            letra='H', numero=1, anio=2015,
            clase=clase, estado=estado, etapa=etapa)

        return expediente

    def test_actualizar_etapa_estado_expediente(self):

        sut = ExpedienteResolucionContratacionCreate()

        expediente = self.get_expediente_object()

        self.assertEqual('PREVENTIVO', expediente.etapa.valor)
        self.assertEqual('RESERVADO', expediente.estado.valor)

        sut.actualizar_etapa_estado_expediente(2, expediente)

        self.assertEqual('COMPROMISO_ORDENADO', expediente.etapa.valor)
        self.assertEqual('CERRADO', expediente.estado.valor)

    def test_guardar_numeros_autoincrementales(self):

        NumeroAutoincremental.objects.create(numero=2, tipo='RESOLUCION_PAGO')

        expediente = self.get_expediente_object()

        expediente_resolucion_contratacion = \
            ExpedienteResolucionContratacion.objects.create(
                expediente=expediente, numero_resolucion=3)

        sut = ExpedienteResolucionContratacionCreate()
        sut.guardar_numeros_autoincrementales(
            expediente_resolucion_contratacion)

        numero_resolucion = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(3, numero_resolucion.numero)

        expediente_resolucion_contratacion.numero_resolucion = 10

        sut.guardar_numeros_autoincrementales(
            expediente_resolucion_contratacion)

        numero_resolucion = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(10, numero_resolucion.numero)

        expediente_resolucion_contratacion.numero_resolucion = 5

        sut.guardar_numeros_autoincrementales(
            expediente_resolucion_contratacion)

        numero_resolucion = NumeroAutoincremental.objects.get(
            tipo='RESOLUCION_PAGO')

        self.assertEqual(10, numero_resolucion.numero)