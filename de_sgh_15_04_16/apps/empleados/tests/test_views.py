
from django.test import TestCase

from apps.complementos.locacion.models import Pais, Provincia, Departamento
from apps.complementos.persona.models import TipoDocumento, Sexo
from apps.complementos.organigrama.models import Profesion
from apps.empleados.models import Empleado, AsignacionFormal
from apps.instituciones.models import Institucion
from apps.personas.models import Persona

from apps.empleados.views import (EmpleadoListView, AsignacionFormalCreate,
                                  AsignacionFormalUpdate,
                                  AsignacionFormalDelete)

# --------------------------------------------------------
# TEST Empleados
# --------------------------------------------------------


class EmpleadoListViewTestCase(TestCase):

    def setUp(self):

        self.empleado_listview = EmpleadoListView()

        TipoDocumento.objects.create(descripcion='Libreta Civica',
                                     longitud=9)
        tipo_documento = TipoDocumento.objects.get(pk=1)

        Profesion.objects.create(nombre='Programador')
        self.profesion = Profesion.objects.get(pk=1)

        Sexo.objects.create(descripcion='Masculino')
        sexo = Sexo.objects.get(pk=1)

        persona = Persona.objects.create(
            nombre='juan',
            apellido='perez',
            tipo_documento=tipo_documento,
            numero_documento='111111111',
            fecha_nacimiento='1900-01-01',
            sexo=sexo,
            profesion=self.profesion
        )

        persona2 = Persona.objects.create(
            nombre='jose',
            apellido='perez',
            tipo_documento=tipo_documento,
            numero_documento='111111111',
            fecha_nacimiento='1900-01-01',
            sexo=sexo,
            profesion=self.profesion
        )

        Empleado.objects.create(persona=persona, fecha_ingreso='1999-01-01',
                                fecha_egreso='1999-01-01')
        Empleado.objects.create(persona=persona2, fecha_ingreso='1999-01-01',
                                fecha_egreso='1999-01-01')

    def tearDown(self):

        del self.empleado_listview
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Profesion.objects.all().delete()
        Sexo.objects.all().delete()

    def test_buscar_por_apellido(self):

        result = self.empleado_listview.buscar_por_apellido('perez')
        self.assertGreater(len(result), 0)

        result = self.empleado_listview.buscar_por_apellido('www')
        self.assertEqual(len(result), 0)

    def test_buscar_por_nombre(self):

        result = self.empleado_listview.buscar_por_nombre('juan')
        self.assertEqual(1, len(result))

        result = self.empleado_listview.buscar_por_nombre('jose')
        self.assertEqual(1, len(result))

        result = self.empleado_listview.buscar_por_nombre('www')
        self.assertEqual(len(result), 0)

    def test_buscar_numero_documento(self):

        result = self.empleado_listview.buscar_por_numero_documento('111111111')
        self.assertGreater(len(result), 0)

        result = self.empleado_listview.buscar_por_numero_documento('222222222')
        self.assertEqual(len(result), 0)

    def test_buscar_por_profesion(self):

        result = self.empleado_listview.buscar_por_profesion('Programador')
        self.assertGreater(len(result), 0)

        result = self.empleado_listview.buscar_por_profesion('Medico')
        self.assertEqual(len(result), 0)

    def test_buscar_por_fecha_ingreso(self):

        result = self.empleado_listview.buscar_por_fecha_ingreso('01/01/1900',
                                                                 '01/01/2000')
        self.assertGreater(len(result), 0)

    def test_buscar_por_fecha_egreso(self):

        result = self.empleado_listview.buscar_por_fecha_egreso('01/01/1900',
                                                                '01/01/2000')
        self.assertGreater(len(result), 0)


# --------------------------------------------------------
# TEST Asignacion Formal de Empleados
# --------------------------------------------------------

class AsignacionFormalCreateTestCase(TestCase):

    def setUp(self):
        self.sut = AsignacionFormalCreate()

        self.institucion = self.get_institucion_object()
        self.empleado = self.get_empleado_object()

    def tearDown(self):
        Persona.objects.all().delete()
        Empleado.objects.all().delete()
        Profesion.objects.all().delete()
        Sexo.objects.all().delete()
        TipoDocumento.objects.all().delete()
        Profesion.objects.all().delete()
        Pais.objects.all().delete()
        Provincia.objects.all().delete()
        Departamento.objects.all().delete()
        Institucion.objects.all().delete()

    def test_asignar_asignacion_formal_empleado(self):

        empleado = self.empleado
        destino = self.institucion

        AsignacionFormal.objects.create(
            empleado=empleado,
            destino=destino,
            fecha_desde='2010-01-01',
            fecha_hasta='2010-12-31',
        )

        empleado_asignacion_formal = self.empleado.asignacionformal_set.all()

        self.assertEqual(1, len(empleado_asignacion_formal))

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

    def get_sexo_object(self):
        sexo = Sexo.objects.create(descripcion='Masculino')

        return sexo

    def get_tipo_documento_object(self):
        tipo_documento = TipoDocumento.objects.create(
            descripcion='DNI', longitud=8)

        return tipo_documento

    def get_profesion_object(self):
        profesion = Profesion.objects.create(nombre='Programador')

        return profesion

    def get_empleado_object(self):

        tipo_documento = self.get_tipo_documento_object()
        profesion = self.get_profesion_object()
        sexo = self.get_sexo_object()

        persona = Persona.objects.create(
            nombre='Fernando',
            apellido='Riquelme',
            tipo_documento=tipo_documento,
            numero_documento='30194000',
            fecha_nacimiento='1983-06-19',
            sexo=sexo,
            profesion=profesion
        )

        empleado = Empleado.objects.create(
            persona=persona, fecha_ingreso='1999-01-01',
            fecha_egreso='1999-01-01')

        return empleado