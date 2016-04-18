
from django.test import TestCase

from apps.complementos.persona.models import TipoDocumento, Sexo
from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.empleados.forms import PersonaForm, EmpleadoForm, AsignacionFormalForm
from apps.instituciones.models import Institucion


class EmpleadoTestCase(TestCase):

    def test_empleado_form(self):

        form = EmpleadoForm()

        self.assertFalse(form.is_valid(), msg='ERROR')

        form_data = {'fecha_ingreso': '10/11/2015'}
        form = EmpleadoForm(form_data)

        self.assertTrue(form.is_valid())

    def test_persona_form(self):

        tipo_documento = TipoDocumento.objects.create(
            descripcion='Libreta Civica', longitud=9)

        form = PersonaForm()

        self.assertFalse(form.is_valid(), msg=form.errors.as_data())

        sexo = Sexo.objects.create(descripcion='Masculino')

        form_data = {
            'apellido': 'Perez',
            'nombre': 'Juan',
            'numero_documento': '111111111',
            'tipo_documento': tipo_documento.id,
            'fecha_nacimiento': '01/01/1900',
            'sexo': sexo.id,
            'foto': 'foto.jpg'
        }

        form = PersonaForm(form_data)

        self.assertTrue(form.is_valid(), msg=form.errors.as_data())

    def test_asignacion_formal_form(self):

        form = AsignacionFormalForm()

        self.assertFalse(form.is_valid(), msg='ERROR: FALTAN CAMPOS REQUERIDOS')

        destino = self.get_institucion_object()

        form_data = {
            'destino': destino.id,
            'fecha_desde': '01/01/2016',
            'fecha_hasta': '31/12/2016',
        }

        form = AsignacionFormalForm(form_data)

        self.assertTrue(form.is_valid())

    def get_institucion_object(self):

        pais = self.get_pais_object()
        provincia = self.get_provincia_object()
        departamento = self.get_departamento_object()

        institucion = Institucion.objects.create(
            nombre='HAC',
            cuit='23301548967',
            telefono='4423568',
            pais=pais,
            provincia=provincia,
            departamento=departamento,
            domicilio='Av Americas y P Gomez'
        )

        return institucion

    def get_pais_object(self):
        pais = Pais.objects.create(nombre='ARG')

        return pais

    def get_provincia_object(self):
        pais = self.get_pais_object()
        provincia = Provincia.objects.create(
            nombre='Formosa',
            pais=pais
        )

        return provincia

    def get_departamento_object(self):
        provincia = self.get_provincia_object()
        departamento = Departamento.objects.create(
            nombre='FSA',
            provincia=provincia
        )

        return departamento




