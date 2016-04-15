from django.test import TestCase

from apps.familiares.forms import FamiliarForm
from apps.familiares import helpers


class FamiliarFormTestCase(TestCase):

    def test_form(self):
        form = FamiliarForm()
        helpers.deshabilitar_campos(form)
        for name, field in form.fields.items():
            self.assertTrue(field.widget.attrs['disabled'] == 'disabled')
