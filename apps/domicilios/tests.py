
from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia

from .forms import DomicilioForm


class DomicilioFormTestCase(TestCase):

    def test_form(self):

        form = DomicilioForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        Pais.objects.create(nombre='Argentina')
        Provincia.objects.create(pais_id=1, nombre='Formosa')

        pais = Pais.objects.all()
        provincia = Provincia.objects.all()

        form_data = {'pais': pais, 'provincia': provincia}

        form = DomicilioForm(form_data)

        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


