# -*- encoding: utf-8 -*-
from django.db import models

from apps.complementos.locacion.models import (Barrio, Pais, Provincia,
                                               Departamento, Localidad)
from apps.personas.models import Persona
#from audit_log.models.managers import AuditLog


class TipoDomicilio(models.Model):
    descripcion = models.CharField(max_length=70)
    # descripcion = models.CharField(max_length=250)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Domicilios"


class Domicilio(models.Model):
    persona = models.ForeignKey(Persona)
    tipo = models.ForeignKey(TipoDomicilio, null=True, blank=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, null=True, blank=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)

    #audit_log = AuditLog()

    def __str__(self):
        return str(self.barrio) + ' - ' + str(self.descripcion)

    class Meta:
        verbose_name_plural = "Domicilios de las Personas"