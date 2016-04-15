
from django.test import TestCase

from apps.familiares.views import FamiliarCreate

from apps.personas.models import Persona
from apps.familiares.models import Familiar, FamiliarPaciente, Parentesco
from apps.pacientes.models import Paciente, TipoPaciente


# --------------------------------------------------------
# TEST familiares
# --------------------------------------------------------


class FamiliarCreateTestCase(TestCase):

    def setUp(self):
        self.sut = FamiliarCreate()
        self.persona = Persona.objects.create(nombre='Prueba',
                                              apellido='Prueba',
                                              fecha_nacimiento='1985-12-08')
        self.tipo_paciente = TipoPaciente.objects.create(descripcion='Prueba',
                                                         abreviatura='P',
                                                         valor='P')
        self.familiar = Familiar.objects.create(persona=self.persona)
        self.paciente = Paciente.objects.create(persona=self.persona,
                                                tipo=self.tipo_paciente)
        self.parentesco = Parentesco.objects.create(
            nombre='Hermano', abreviatura='H')

        self.familiar_paciente = FamiliarPaciente.objects.create(
            familiar=self.familiar, paciente=self.paciente,
            parentesco=self.parentesco)

    def tearDown(self):
        Persona.objects.all().delete()
        Familiar.objects.all().delete()
        TipoPaciente.objects.all().delete()
        Paciente.objects.all().delete()

    def test_guardar_persona(self):
        self.assertTrue(self.persona)

    def test_guardar_parentesco(self):
        self.assertTrue(self.parentesco)

    def test_guardar_parentesco_fail(self):
        self.parentesco = Parentesco.objects.create()
        self.assertFalse(self.parentesco.save())

    def test_guardar_familiar(self):
        self.assertTrue(self.familiar)

    def test_guardar_paciente(self):
        self.assertTrue(self.paciente)

    def test_guardar_familiar_paciente(self):
        self.assertTrue(self.familiar_paciente)
