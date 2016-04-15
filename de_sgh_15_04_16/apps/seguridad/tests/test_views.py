# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.seguridad.models import Perfil
from apps.seguridad.views import PerfilListView


class PerfilListViewTestCase(TestCase):

    def test_buscar_por_nombre(self):

        self.sut = PerfilListView()

        result = self.sut.buscar_por_nombre('ADMINISTRADOR')
        self.assertEqual(0, len(result))

        Perfil.objects.create(nombre='ADMINISTRADOR')
        Perfil.objects.create(nombre='EDITOR')
        Perfil.objects.create(nombre='ADMISION')

        result = self.sut.buscar_por_nombre('ADMINISTRADOR')
        self.assertEqual(1, len(result))
        self.assertEqual('ADMINISTRADOR', result[0].nombre)

        result = self.sut.buscar_por_nombre('ADMI')
        self.assertEqual(2, len(result))
        self.assertEqual('ADMINISTRADOR', result[0].nombre)
        self.assertEqual('ADMISION', result[1].nombre)