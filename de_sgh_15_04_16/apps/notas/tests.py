from django.test import TestCase

from .forms import NotaForm
from .models import TipoNota


class DomicilioFormTestCase(TestCase):

    def test_form(self):

        form = NotaForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        TipoNota.objects.create(descripcion='Documentación del Paciente')

        tipo_nota = TipoNota.objects.all()

        form_data = {'descripcion': 'Prueba de Nota',
                     'tipo_nota': tipo_nota}

        form = NotaForm(form_data)

        self.assertTrue(form.is_valid(), msg=form.errors.as_data())
