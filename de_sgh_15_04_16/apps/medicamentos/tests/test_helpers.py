
from django.test import TestCase
from django.test.client import RequestFactory

from apps.medicamentos import helpers
from apps.medicamentos.models import Catalogo, NumeroAutoincremental


class HelpersTestCase(TestCase):

    def crear_numeros_autoincrementales(self):
        catalogo = Catalogo.objects.create(descripcion='MEDICAMENTO')
        NumeroAutoincremental.objects.create(numero=0, tipo=catalogo)

    def test_get_numero_autoincremental(self):

        self.crear_numeros_autoincrementales()

        numero = helpers.get_numero_autoincremental('MEDICAMENTO')
        self.assertEqual(1, numero)

    def test_guardar_numero_autoincremental(self):

        self.crear_numeros_autoincrementales()

        helpers.guardar_numero_autoincremental('MEDICAMENTO', 1)
        numero = helpers.get_numero_autoincremental('MEDICAMENTO')

        self.assertEqual(2, numero)

    def test_registrar_numeros_autoincrementales(self):

        self.crear_numeros_autoincrementales()

        listado = {
            'MEDICAMENTO': 1,
        }

        helpers.registrar_numeros_autoincrementales(listado)

        numero = helpers.get_numero_autoincremental('MEDICAMENTO')
        self.assertEqual(2, numero)

    def test_set_id_medicamento(self):

        self.factory = RequestFactory()
        self.request = self.factory.get('/medicamentos/laboratorios/alta/1')
        self.request = helpers.set_id_medicamento(self.request, 1)
        self.assertEqual(1, self.request['medicamento'])
