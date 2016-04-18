from datetime import datetime

from django.test import TestCase

from apps.complementos.obrasocial.models import ObraSocial
from apps.complementos.paciente.models import Categoria

from .helpers import *

from .forms import PersonaObraSocialForm
from .models import Persona


class DetallePersonaObraSocial(TestCase):

    def test_form(self):

        form = PersonaObraSocialForm()
        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        obrasocial = ObraSocial.objects.create(
            nombre='OSPAT', codigo_padron=20)

        categoria = Categoria.objects.create(descripcion='A1')

        numeroafiliado = 10203000
        beneficiario = 'T'
        fechaemision = '14/01/2000'
        fechavencimiento = '14/01/2020'

        form_data = {
            'obra_social': obrasocial.id,
            'numero_afiliado': numeroafiliado,
            'tipo_beneficiario': beneficiario,
            'categoria': categoria.id,
            'fecha_emision': fechaemision,
            'fecha_vencimiento': fechavencimiento,
        }

        form = PersonaObraSocialForm(form_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_data())


class TestPersonaModel(TestCase):

    def test_get_edad(self):

        persona = Persona()

        persona.fecha_nacimiento = datetime.strptime(
            str('1981-05-01'), "%Y-%m-%d").date()
        edad = persona.get_edad()

        self.assertEqual(34, edad)

        persona.fecha_nacimiento = datetime.strptime(
            str('1981-01-01'), "%Y-%m-%d").date()
        edad = persona.get_edad()

        self.assertEqual(35, edad)


class TestHelper(TestCase):

    def test_existe_registro_persona_obra_social(self):

        categoria = Categoria.objects.create(descripcion='A1')

        obrasocial = ObraSocial.objects.create(nombre='OSDE', codigo_padron=200)

        persona = Persona.objects.create(nombre='Juan', apellido='Perez',
            obra_social=obrasocial)

        result = existe_registro_persona_obra_social(
            persona, obrasocial)

        self.assertFalse(result)

        PersonaObraSocial.objects.create(persona=persona,
            categoria=categoria, obra_social=obrasocial)

        result = existe_registro_persona_obra_social(
            persona, obrasocial)

        self.assertTrue(result)
