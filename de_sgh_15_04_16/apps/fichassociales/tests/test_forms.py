from datetime import datetime
from django.test import TestCase

from apps.complementos.IVA.models import TipoIVA
from apps.fichassociales.forms import FichaSocialForm


class FichaSocialFormTest(TestCase):

    def test_form(self):

        form = FichaSocialForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        ultima_verificacion = datetime.now()

        TipoIVA.objects.create(descripcion='Monotributista')

        tipo_iva = TipoIVA.objects.all()

        form_data = {'numero_ficha': '614325',
                     'ultima_verificacion': ultima_verificacion,
                     'tipo_iva': tipo_iva}

        form = FichaSocialForm(form_data)

        self.assertTrue(form.is_valid(), msg=form.errors.as_data())
