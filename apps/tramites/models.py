from datetime import datetime
from django.db import models

from apps.complementos.organigrama.models import Entidad
from apps.clientes.models import Cliente


class TipoTramite(models.Model):
    descripcion = models.CharField(max_length=50)
    entidad = models.ForeignKey(Entidad, null=True, blank=True)

    def __str__(self):
        return self.descripcion + ' - ' + str(self.entidad)

    class Meta:
        verbose_name_plural = "Tipos de Tramite"


class Requisito(models.Model):
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    valor = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Requisitos"


class RequisitoTipoTramite(models.Model):
    tipo_tramite = models.ForeignKey(TipoTramite, null=False, blank=True)
    requisito = models.ForeignKey(Requisito, null=False, blank=True)

    def __str__(self):
        return str(self.tipo_tramite) + '-' + str(self.requisito)

    class Meta:
        verbose_name_plural = "Requisitos del Tipo de Tramite"


class Tramite(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    tipo = models.ForeignKey(TipoTramite, null=True, blank=True)
    fecha_alta = models.DateTimeField(default=datetime.now, null=True,
                                      blank=True)
    fecha_turno = models.DateField(null=True, blank=True)
    fecha_alarma = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.BooleanField(default=False, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.tipo)

    class Meta:
        verbose_name_plural = "Tramites"


class RequisitoTramite(models.Model):
    tramite = models.ForeignKey(Tramite, null=False, blank=True)
    requisito = models.ForeignKey(Requisito, null=False, blank=True)
    presentado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tramite) + '-' + str(self.requisito) + '-' + \
            str(self.presentado)

    class Meta:
        verbose_name_plural = "Requisitos Requeridos del Tramite"