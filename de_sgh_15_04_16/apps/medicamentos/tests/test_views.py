# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.medicamentos.models import (Catalogo, PrincipioActivo, Medicamento,
                                      NumeroAutoincremental)
from apps.medicamentos import helpers

from apps.medicamentos.views import (MedicamentoCreate, MedicamentoUpdate)
from apps.complementos.salud.models import UnidadMedida

# --------------------------------------------------------
# TEST Medicamento
# --------------------------------------------------------


class MedicamentoCreateTestCase(TestCase):

    def setUp(self):
        self.sut = MedicamentoCreate()

        self.catalogo = Catalogo.objects.create(descripcion='MEDICAMENTO')
        NumeroAutoincremental.objects.create(numero=0, tipo=self.catalogo)

        PrincipioActivo.objects.create(descripcion="Amoxicilina")
        PrincipioActivo.objects.create(descripcion="Acido Clavulonico")
        UnidadMedida.objects.create(descripcion="mg")
        UnidadMedida.objects.create(descripcion="ml")

        self.medicamento = self.get_medicamento_object()

    def tearDown(self):
        Catalogo.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()

    def get_medicamento_object(self):

        codigo = helpers.get_numero_autoincremental('MEDICAMENTO')

        medicamento = Medicamento.objects.create(
            catalogo=self.catalogo,
            codigo=codigo,
            denominacion='Amoxicilina',
            producto_combinado=True,
            libre_gluten=True
        )

        return medicamento

    def test_medicamento_create(self):

        self.assertEqual('MEDICAMENTO', self.medicamento.catalogo.descripcion)
        self.assertEqual(1, self.medicamento.codigo)

    def test_guardar_items_composicion(self):

        datos_composicion = [
            {
                'principio_activo': 'Amoxicilina',
                'potencia_numerador': '888 mg',
                'potencia_denominador': '1 ml'
            }
        ]

        self.sut.guardar_items_composicion(datos_composicion, self.medicamento)

        items_composicion = \
            self.medicamento.composicion_set.all()

        self.assertNotEqual(2, len(items_composicion))
        self.assertEqual(1, len(items_composicion))


class MedicamentoUpdateTestCase(TestCase):

    def setUp(self):
        self.sut = MedicamentoUpdate()

        self.catalogo = Catalogo.objects.create(descripcion='MEDICAMENTO')

        NumeroAutoincremental.objects.create(numero=0, tipo=self.catalogo)

    def tearDown(self):
        Catalogo.objects.all().delete()
        NumeroAutoincremental.objects.all().delete()

    def get_medicamento_object(self):

        codigo = helpers.get_numero_autoincremental('MEDICAMENTO')

        medicamento = Medicamento.objects.create(
            catalogo=self.catalogo,
            codigo=codigo,
            denominacion='Amoxicilina',
            producto_combinado=True,
            libre_gluten=True
        )

        return medicamento

    def test_medicamento_update(self):

        medicamento = self.get_medicamento_object()

        self.assertEqual('Amoxicilina', medicamento.denominacion)

        medicamento.denominacion = 'Amoxicilina2'
        medicamento.save()

        self.assertEqual('Amoxicilina2', medicamento.denominacion)

