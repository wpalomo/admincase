
from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento

from .forms import InstitucionForm


class InstitucionTestCase(TestCase):

    def test_institucion_form(self):

        form = InstitucionForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        pais = Pais.objects.create(nombre='Argentina')
        provincia = Provincia.objects.create(
            nombre='Formosa', pais=pais)
        departamento = Departamento.objects.create(
            nombre='Pilcomayo', provincia=provincia)

        form_data = {
            'nombre': '10/11/2015',
            'cuit': '10/11/2015',
            'pais': pais.id,
            'provincia': provincia.id,
            'departamento': departamento.id
        }

        form = InstitucionForm(form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())