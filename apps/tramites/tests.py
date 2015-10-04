from django.test import TestCase

from apps.personas.models import Persona
from apps.complementos.persona.models import TipoDocumento
from apps.complementos.organigrama.models import Entidad
from .models import Tramite, TipoTramite


class TramiteTest(TestCase):

    def test_crear_tramite(self):
        # self.assertEqual(1 + 3, 2)
        TipoDocumento.objects.create(
            descripcion='DNI',
            abreviatura='DNI'
        )

        tipo_documento = TipoDocumento.objects.get(pk=1)

        persona = Persona.objects.create(
            nombre='JUAN',
            apellido='PEREZ',
            tipo_documento=tipo_documento,
            numero_documento='30194000',
            fecha_nacimiento='1900-01-01'
        )

# persona = models.ForeignKey(Persona)
# tipo = models.ForeignKey(TipoTramite)
# estado = models.BooleanField(default=False, blank=True)
# observacio

        Entidad.objects.create(
            nombre='ANSES'
        )

        entidad = Entidad.objects.get(pk=1)

        TipoTramite.objects.create(
            nombre='JUBILACION ORDINARIA',
            entidad=entidad
        )

        TipoTramite.objects.create(
            nombre='JUBILACION POR INVALIDEZ',
            entidad=entidad
        )

        tipo_tramite_1 = TipoTramite.objects.get(pk=1)
        tipo_tramite_2 = TipoTramite.objects.get(pk=2)

        Tramite.objects.create(
            persona=persona,
            tipo=tipo_tramite_1,
            observaciones='ok'
        )

        Tramite.objects.create(
            persona=persona,
            tipo=tipo_tramite_2,
            observaciones='ok'
        )

        tramite = Tramite.objects.all()
#
        print(tramite)


