from django.db import models

from apps.complementos.organigrama.models import Entidad
from apps.personas.models import Persona


class TipoTramite(models.Model):
    nombre = models.CharField(max_length=30)
    estado = models.BooleanField(default=False, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Tramite"


class Tramite(models.Model):
    persona = models.ForeignKey(Persona)
    tipo = models.ForeignKey(TipoTramite, null=True, blank=True)
    entidad = models.ForeignKey(Entidad)

    def __str__(self):
        return str(self.tipo) + ' - ' + str(self.entidad)

    class Meta:
        verbose_name_plural = "Tramites"