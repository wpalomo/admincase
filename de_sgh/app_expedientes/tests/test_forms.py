# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.empleados.models import Empleado
from apps.expedientes.forms import (ExpedienteForm, ExpedienteResolucionForm,
                                    ExpedienteDisposicionForm,
                                    ExpedienteServicioMedicoForm,
                                    ExpedienteLicitacionForm,
                                    ExpedienteComodatoForm)
from apps.personas.models import Persona
from apps.expedientes import helpers

from apps.expedientes.models import (Estado, Clase, Etapa, FuenteFinanciamiento,
                                     NumeroAutoincremental)
from apps.proveedores.models import Proveedor


class ExpedienteFormTestCase(TestCase):

    def setUp(self):
        estado = Estado.objects.create(descripcion='Inicio')
        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)
        clase = Clase.objects.create(descripcion='Inicio')

        self.data = {
            'letra': 'H',
            'numero': 1,
            'anio': 15,
            'fecha': '15/08/2015',
            'estado': estado.id,
            'empleado_solicitante': empleado.id,
            'clase': clase.id
        }

    def tearDown(self):
        Estado.objects.all().delete()
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Clase.objects.all().delete()

    def test_form(self):

        form = ExpedienteForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = ExpedienteForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    # ----------------------------------------------------
    # Tests generados por errores enviados desde Testing
    # ----------------------------------------------------

    def test_fecha_mayor_a_actual(self):

        self.data['fecha'] = '20/01/2080'

        form = ExpedienteForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())


class ExpedienteResolucionFormTestCase(TestCase):

    def setUp(self):

        # Objetos NumeroAutoincremental, necesarios para que el form
        # los utilice para los valores iniciales de los campos:
        # propiedad initial de los campos del formulario

        NumeroAutoincremental.objects.create(
            numero=0, tipo='RESOLUCION_ADJUDICACION')
        NumeroAutoincremental.objects.create(numero=0, tipo='ORDEN_PROVISION')
        NumeroAutoincremental.objects.create(numero=0, tipo='ACTA_RECEPCION')

        proveedor = Proveedor.objects.create(razon_social='Camiletti')
        etapa = Etapa.objects.create(descripcion='Inicio', resolucion=1)
        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        self.data = {
            'etapa': etapa.id,
            'resolucion_adjudicacion': 1,
            'fecha_resolucion_adjudicacion': '1/10/2015',
            'numero_resolucion_pago': 1,
            'fecha_resolucion_pago': '01/01/1900',
            'proveedor': proveedor.id,
            'importe': 0,
            'orden_provision': 1,
            'acta_recepcion': 1,
            'tipo_transaccion': 'COMPRA DIRECTA',
            'numero_identificacion_transaccion': 10,
            'fuente_financiamiento': fuente_financiamiento.id
        }

    def tearDown(self):
        NumeroAutoincremental.objects.all().delete()
        Proveedor.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()

    def test_form(self):

        form = ExpedienteResolucionForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = ExpedienteResolucionForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    # ----------------------------------------------------
    # Tests generados por errores enviados desde Testing
    # ----------------------------------------------------

    def test_fecha_resolucion_pago_mayor_a_actual(self):

        self.data['fecha_resolucion_pago'] = '20/01/2080'

        form = ExpedienteResolucionForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

    def test_fecha_resolucion_adjudicacion_mayor_a_actual(self):

        self.data['fecha_resolucion_adjudicacion'] = '20/01/2080'

        form = ExpedienteResolucionForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())


class ExpedienteDisposicionFormTestCase(TestCase):

    def setUp(self):
        NumeroAutoincremental.objects.create(numero=0,
                                             tipo='CONTRATACION_DIRECTA')
        NumeroAutoincremental.objects.create(numero=0,
                                             tipo='NUMERO_DISPOSICION')

        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='2525')
        proveedor = Proveedor.objects.create(razon_social='AGUA DEL NORTE')
        etapa = Etapa.objects.create(
            descripcion='preventivo', valor='PREVENTIVO', disposicion=1)

        contratacion_directa = helpers.get_numero_autoincremental(
            'CONTRATACION_DIRECTA')
        numero_disposicion = helpers.get_numero_autoincremental(
            'NUMERO_DISPOSICION')

        self.data = {
            'etapa': etapa.id,
            'contratacion_directa': contratacion_directa,
            'numero_disposicion': numero_disposicion,
            'fuente_financiamiento': fuente_financiamiento.id,
            'fecha_disposicion': '25/09/2015',
            'proveedor': proveedor.id,
            'importe': '1199.0',
            'observaciones': 'todoOk'
        }

    def tearDown(self):
        NumeroAutoincremental.objects.all().delete()
        Proveedor.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()

    def test_form(self):

        form = ExpedienteDisposicionForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = ExpedienteDisposicionForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    # -------------------------------------------------------
    # Tests generados por errores enviados desde Testing #866
    # -------------------------------------------------------

    def test_fecha_disposicion_mayor_a_actual(self):

        self.data['fecha_disposicion'] = '20/01/2080'

        form = ExpedienteDisposicionForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())


class ExpedienteServicioMedicoFormTestCase(TestCase):

    def setUp(self):
        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)
        etapa = Etapa.objects.create(descripcion='ejemplo', servicio_medico=1)
        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        self.data = {
            'etapa': etapa.id,
            'profesional': empleado.id,
            'resolucion_contratacion': 'AXZY001',
            'fecha_resolucion_contratacion': '1/10/2015',
            'orden_provision': 1,
            'acta_recepcion': 1,
            'numero_resolucion_pago': 1,
            'fecha_resolucion_pago': '1/10/2015',
            'importe': 100,
            'solicitante_resolucion_pago': empleado.id,
            'fuente_financiamiento': fuente_financiamiento.id
        }

    def tearDown(self):
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()

    def test_form(self):

        form = ExpedienteServicioMedicoForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = ExpedienteServicioMedicoForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    # ----------------------------------------------------
    # Tests generados por errores enviados desde Testing
    # ----------------------------------------------------

    def test_fecha_resolucion_contratacion_mayor_a_actual(self):

        self.data['fecha_resolucion_contratacion'] = '20/01/2080'

        form = ExpedienteServicioMedicoForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

    def test_fecha_resolucion_pago_mayor_a_actual(self):

        self.data['fecha_resolucion_pago'] = '20/01/2080'

        form = ExpedienteServicioMedicoForm(self.data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())


class ExpedienteComodatoFormTestCase(TestCase):

    def setUp(self):
        proveedor = Proveedor.objects.create(razon_social='AGUA DEL NORTE')
        fuente_financiamiento = FuenteFinanciamiento.objects.create(cuenta='BBVA', fondo='1212')
        persona = Persona.objects.create(apellido='perez', nombre='juan')
        empleado = Empleado.objects.create(persona=persona)

        self.data = {
            'observaciones':'sdfsdfa asdf asd',
            'proveedor':proveedor,
            'fecha_resolucion_contratacion':'10/10/2015',
            'resolucion_contratacion':1,
            'resolucion_pago':1,
            'solicitante_resolucion_pago':empleado.id,
            'fuente_financiamiento':fuente_financiamiento.id,
            'numero_contratacion_directa':1,
            'orden_provision':1,
            'fecha_resolucion_pago':'10/10/2015',
            'importe':1}


class ExpedienteLicitacionFormTestCase(TestCase):

    def setUp(self):

        NumeroAutoincremental.objects.create(
            numero=0, tipo='NUMERO_DISPOSICION')
        NumeroAutoincremental.objects.create(numero=0, tipo='NUMERO_LICITACION')
        NumeroAutoincremental.objects.create(
            numero=0, tipo='RESOLUCION_ADJUDICACION')
        NumeroAutoincremental.objects.create(numero=0, tipo='RESOLUCION_PAGO')

        etapa = Etapa.objects.create(descripcion='compromiso', licitacion=1)
        fuente_financiamiento = FuenteFinanciamiento.objects.create(
            cuenta='BBVA', fondo='1212')

        numero_disposicion = helpers.get_numero_autoincremental(
            'NUMERO_DISPOSICION')

        numero_licitacion = helpers.get_numero_autoincremental(
            'NUMERO_LICITACION')

        resolucion_adjudicacion = helpers.get_numero_autoincremental(
            'RESOLUCION_ADJUDICACION')

        self.data = {
            'etapa': etapa.id,
            'numero': numero_licitacion,
            'anio': '15',
            'numero_disposicion': numero_disposicion,
            'resolucion_aprobacion': '1',
            'fecha_resolucion_aprobacion': '1/10/2015',
            'resolucion_adjudicacion': resolucion_adjudicacion,
            'fecha_resolucion_adjudicacion': '1/10/2015',
            'fuente_financiamiento': fuente_financiamiento.id
        }

    def tearDown(self):
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Etapa.objects.all().delete()
        FuenteFinanciamiento.objects.all().delete()
        Proveedor.objects.all().delete()

    def test_form(self):
        form = ExpedienteComodatoForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = ExpedienteLicitacionForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())