
from django.test import TestCase

from apps.complementos.persona.models import TipoDocumento, Sexo


from apps.pacientes.forms import PacienteForm, PersonaForm
from apps.pacientes.models import TipoPaciente


class PacienteTestCase(TestCase):

    def test_paciente_form(self):

        tipo_paciente = TipoPaciente.objects.create(descripcion='Normal')

        form = PacienteForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        form_data = {'tipo': tipo_paciente.id}
        form = PacienteForm(form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    def test_persona_form(self):

        form = PersonaForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        tipo_documento = TipoDocumento.objects.create(
            descripcion='Libreta Civica', longitud=9)
        sexo = Sexo.objects.create(descripcion='Masculino')

        form_data = {
            'tipo_documento': tipo_documento.id,
            'fecha_nacimiento': '1900-01-01',
            'sexo': sexo.id
        }

        form = PersonaForm(form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())