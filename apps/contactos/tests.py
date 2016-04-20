from django.test import TestCase

from .forms import ContactoForm
from .models import TipoContacto


class DomicilioFormTestCase(TestCase):

    def test_form(self):

        form = ContactoForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        TipoContacto.objects.create(descripcion='SITIO WEB')

        tipo_contacto = TipoContacto.objects.all()

        form_data = {'descripcion': 'www.prueba.com.ar',
                     'tipo_contacto': tipo_contacto}

        form = ContactoForm(form_data)

        self.assertTrue(form.is_valid(), msg=form.errors.as_data())
