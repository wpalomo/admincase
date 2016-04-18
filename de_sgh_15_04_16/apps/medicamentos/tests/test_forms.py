# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.medicamentos.forms import (MedicamentoForm,
                                     MedicamentoLaboratorioForm)

from apps.medicamentos.models import (Catalogo, NumeroAutoincremental,
                                      Medicamento, Laboratorio,
                                      FormaFarmaceutica, ViaAdministracion,
                                      Envase, Pack, UnidadMedida)


class MedicamentoFormTestCase(TestCase):

    def setUp(self):
        catalogo = Catalogo.objects.create(descripcion='MEDICAMENTO')
        NumeroAutoincremental.objects.create(numero=0, tipo=catalogo)

        self.data = {
            'catalogo': catalogo.id,
            'codigo': 1,
            'denominacion': 'Amoxicilina',
            'producto_combinado': True
        }

    def tearDown(self):
        Catalogo.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()

    def test_form(self):
        form = MedicamentoForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = MedicamentoForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class MedicamentoLaboratorioFormTestCase(TestCase):

    def setUp(self):
        catalogo = Catalogo.objects.create(descripcion='MEDICAMENTO')
        NumeroAutoincremental.objects.create(numero=0, tipo=catalogo)
        medicamento = Medicamento.objects.create(catalogo=catalogo, codigo=1,
                                                 denominacion='Amoxilina',
                                                 producto_combinado=True)
        laboratorio = Laboratorio.objects.create(descripcion='Laboratorio A')
        via_administracion = ViaAdministracion.objects.create(
            descripcion='Administración')
        forma_farmaceutica = FormaFarmaceutica.objects.create(
            via_administracion=via_administracion, descripcion='Administración')
        envase = Envase.objects.create(descripcion='TABLETA')
        pack = Pack.objects.create(descripcion='Agrupados')
        unidad_medida = UnidadMedida.objects.create(descripcion='cápsulas')

        self.data_errors = {
            'medicamento': medicamento.id,
            'nombre_comercial': 'OPTAMOX DUO',
            'laboratorio': laboratorio.id,
            'forma_farmaceutica': forma_farmaceutica.id,
            'envase_primario': envase.id,
            'cantidad_envase_primario': 2,
            'pack_unidad_despacho': pack.id
        }

        self.data = {
            'medicamento': medicamento.id,
            'nombre_comercial': 'OPTAMOX DUO',
            'laboratorio': laboratorio.id,
            'forma_farmaceutica': forma_farmaceutica.id,
            'envase_primario': envase.id,
            'cantidad_envase_primario': 2,
            'pack_cantidad': 3,
            'pack_unidad_despacho': pack.id,
            'unidad_medida_envase_primario': unidad_medida.id
        }

    def tearDown(self):
        Catalogo.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()
        Medicamento.objects.all().delete()
        Laboratorio.objects.all().delete()
        ViaAdministracion.objects.all().delete()
        FormaFarmaceutica.objects.all().delete()
        Envase.objects.all().delete()
        Pack.objects.all().delete()
        UnidadMedida.objects.all().delete()

    def test_form(self):
        form = MedicamentoLaboratorioForm(self.data_errors)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form = MedicamentoLaboratorioForm(self.data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())
