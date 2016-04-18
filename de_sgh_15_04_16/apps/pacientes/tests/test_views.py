
from django.test import TestCase

from apps.complementos.persona.models import TipoDocumento
from apps.pacientes.models import Paciente, TipoPaciente
from apps.pacientes.views import PacienteListView
from apps.personas.models import Persona

# --------------------------------------------------------
# TEST Paciente
# --------------------------------------------------------


class PacienteListViewTestCase(TestCase):

    def setUp(self):

        self.paciente_listview = PacienteListView()

        TipoDocumento.objects.create(descripcion='Libreta Civica',
                                     longitud=9)
        tipo_documento = TipoDocumento.objects.get(pk=1)

        persona = Persona.objects.create(
            nombre='juan',
            apellido='perez',
            tipo_documento=tipo_documento,
            numero_documento='111111111',
            fecha_nacimiento='1900-01-01'
        )

        persona2 = Persona.objects.create(
            nombre='maria',
            apellido='perez',
            tipo_documento=tipo_documento,
            numero_documento='333',
            fecha_nacimiento='1900-01-01'
        )

        tipo_paciente = TipoPaciente.objects.create(descripcion='Normal')

        Paciente.objects.create(persona=persona, tipo=tipo_paciente)
        Paciente.objects.create(persona=persona2, tipo=tipo_paciente)

    def tearDown(self):

        del self.paciente_listview
        Persona.objects.all().delete()
        Paciente.objects.all().delete()

    def test_buscar_por_apellido(self):

        result = self.paciente_listview.buscar_por_apellido('lopez')
        self.assertEqual(0, len(result))

        result = self.paciente_listview.buscar_por_apellido('perez')
        self.assertEqual(2, len(result))
        self.assertGreater(len(result), 0)

    def test_buscar_por_nombre(self):

        result = self.paciente_listview.buscar_por_nombre('jose')
        self.assertEqual(0, len(result))

        result = self.paciente_listview.buscar_por_nombre('juan')
        self.assertEqual(1, len(result))

    def test_buscar_por_numero_documento(self):

        result = self.paciente_listview.buscar_por_numero_documento('000')
        self.assertEqual(0, len(result))

        result = self.paciente_listview.buscar_por_numero_documento('111111111')
        self.assertEqual(1, len(result))

    def test_buscar_por_codigo_paciente(self):

        result = self.paciente_listview.buscar_por_codigo_paciente('100')
        self.assertEqual(0, len(result))

        result = self.paciente_listview.buscar_por_codigo_paciente('1')
        self.assertEqual(1, len(result))

    def test_buscar_por_nombre_apellido(self):

        result = self.paciente_listview.buscar_por_nombre_apellido(
            'jose', 'perez')
        self.assertEqual(0, len(result))

        result = self.paciente_listview.buscar_por_nombre_apellido(
            'juan', 'perez')
        self.assertEqual(1, len(result))

