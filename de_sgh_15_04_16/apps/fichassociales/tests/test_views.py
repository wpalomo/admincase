
from django.test import TestCase

from apps.fichassociales.views import FichaSocialCreate

from apps.fichassociales.models import FichaSocial
from apps.complementos.IVA.models import TipoIVA
from apps.personas.models import Persona
from apps.pacientes.models import Paciente, TipoPaciente


# --------------------------------------------------------
# TEST familiares
# --------------------------------------------------------


class FichaSocialCreateTestCase(TestCase):

    def setUp(self):

        self.sut = FichaSocialCreate()
        self.persona = Persona.objects.create(nombre='Prueba',
                                              apellido='Prueba',
                                              fecha_nacimiento='1985-12-08')
        self.tipo_paciente = TipoPaciente.objects.create(descripcion='Prueba',
                                                         abreviatura='P',
                                                         valor='P')

        self.paciente = Paciente.objects.create(persona=self.persona,
                                                tipo=self.tipo_paciente)

        self.tipo_iva = TipoIVA.objects.create(descripcion='Monotributista')

        self.ficha_social = FichaSocial.objects.create(paciente=self.paciente,
                                                       numero_ficha='12345678',
                                                       tipo_iva=self.tipo_iva)

    def tearDown(self):
        Persona.objects.all().delete()
        FichaSocial.objects.all().delete()
        TipoPaciente.objects.all().delete()
        Paciente.objects.all().delete()

    def test_guardar_persona(self):
        self.assertTrue(self.persona)

    def test_guardar_paciente(self):
        self.assertTrue(self.paciente)

    def test_guardar_tipo_iva(self):
        self.assertTrue(self.tipo_iva)

    def test_guardar_ficha_social(self):
        self.assertTrue(self.ficha_social)

