from django.db import models

from apps.complementos.organigrama.models import Entidad
from apps.personas.models import Persona


class Requisito(models.Model):
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Requisitos de Tramite"


class TipoTramite(models.Model):
    descripcion = models.CharField(max_length=30)
    entidad = models.ForeignKey(Entidad)
    requisitos = models.ManyToManyField(Requisito)

    def __str__(self):
        return self.descripcion + ' - ' + str(self.entidad)

    class Meta:
        verbose_name_plural = "Tipos de Tramite"


class Tramite(models.Model):
    persona = models.ForeignKey(Persona)
    tipo = models.ForeignKey(TipoTramite)
    estado = models.BooleanField(default=False, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.tipo)

    class Meta:
        verbose_name_plural = "Tramites"


class RequisitoPresentado(models.Model):
    tramite = models.ForeignKey(Tramite, null=True, blank=True)
    requisito = models.ForeignKey(Requisito, null=True, blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tramite) + '-' + str(self.requisito) + '-' + str(self.estado)
