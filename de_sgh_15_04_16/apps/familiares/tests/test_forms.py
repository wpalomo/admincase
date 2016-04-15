from django.test import TestCase

from apps.complementos.locacion.models import LugarNacimiento, Pais
from apps.familiares.models import Parentesco
from apps.complementos.persona.models import Sexo, TipoDocumento

from apps.familiares.forms import FamiliarForm, FamiliarPacienteForm, \
    LugarNacimientoForm, PersonaForm


class FamiliarFormTestCase(TestCase):

    def test_form(self):

        form = FamiliarForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form_data = {'vive': True}
        form = FamiliarForm(form_data)
        self.assertTrue(form.is_valid())


class FamiliarPacienteFormTestCase(TestCase):

    def test_form(self):

        form = FamiliarPacienteForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        Parentesco.objects.create(nombre='Hermano',
                                  abreviatura='H')
        parentesco = Parentesco.objects.all()
        form_data = {'parentesco': parentesco}
        form = FamiliarPacienteForm(form_data)
        self.assertTrue(form.is_valid())


class LugarNacimientoFormTestCase(TestCase):

    def test_form(self):

        form = LugarNacimientoForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())
        Pais.objects.create(nombre='Argentina')
        pais = Pais.objects.all()
        form_data = {'pais': pais}
        form = LugarNacimientoForm(form_data)
        self.assertTrue(form.is_valid())


class PersonaFormTestCase(TestCase):

    def test_form(self):

        form = PersonaForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        Sexo.objects.create(descripcion='Masculino', abreviatura='M')
        TipoDocumento.objects.create(descripcion='Documento', abreviatura='DNI',
                                     longitud=10)
        tipo_documento = TipoDocumento.objects.all()
        sexo = Sexo.objects.all()
        form_data = {'sexo': sexo, 'tipo_documento': tipo_documento,
                     'numero_documento': '31897427',
                     'fecha_nacimiento': '08/12/1985'}
        form = PersonaForm(form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())
        form_data = {'sexo': sexo}
        form = PersonaForm(form_data)
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())
