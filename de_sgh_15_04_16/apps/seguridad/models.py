# -*- encoding: utf-8 -*-

from django.db import models

from apps.complementos.arbolitem.models import ArbolItem
from apps.empleados.models import Empleado
from apps.instituciones.models import Institucion


class Perfil(models.Model):
    institucion = models.ForeignKey(
        Institucion, unique=False, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    valor = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Perfiles"


class PerfilModulo(models.Model):

    perfil = models.ForeignKey(Perfil, unique=False)
    modulo = models.ForeignKey(ArbolItem, unique=False)

    class Meta:
        verbose_name_plural = "Perfiles-Modulos"


class EmpleadoAgenda(models.Model):
    empleado = models.ForeignKey(Empleado)
    tiene_agenda = models.BooleanField(default=True)

    def __str__(self):
        return str(self.empleado)

    class Meta:
        verbose_name_plural = "Permisos Empleado-Agenda"