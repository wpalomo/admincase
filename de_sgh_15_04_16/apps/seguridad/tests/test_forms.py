# -*- coding: utf-8 -*-

from django.test import TestCase

from apps.complementos.arbolitem.models import ArbolItem
from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.instituciones.models import Institucion
from apps.seguridad.forms import PerfilForm, PerfilModuloForm
from apps.seguridad.models import Perfil


class PerfilFormTestCase(TestCase):

    def test_form(self):

        form = PerfilForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        pais = Pais.objects.create(nombre='Argentina')
        provincia = Provincia.objects.create(nombre='Formosa', pais=pais)
        departamento = Departamento.objects.create(
            nombre='Formosa', provincia=provincia)

        instituto = Institucion.objects.create(
            nombre='Evita',
            cuit='2020',
            pais=pais,
            provincia=provincia,
            departamento=departamento
            )

        data = {'institucion': instituto.id, 'nombre': 'Administrador'}

        form = PerfilForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class PerfilModuloFormTestCase(TestCase):

    def test_form(self):

        form = PerfilModuloForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        perfil = Perfil.objects.create(nombre='ADMISION')
        modulo = ArbolItem.objects.create(
            descripcion='FARMACIA',
            padre_id=0,
            visible=True,
            is_folder=True
            )

        data = {'perfil': perfil.id, 'modulo': modulo.id}

        form = PerfilModuloForm(data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())