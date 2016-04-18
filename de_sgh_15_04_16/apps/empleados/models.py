# -*- encoding: utf-8 -*-

from django.db import models

from apps.complementos.organigrama.models import (Cargo, Direccion,
                                                  Departamento, Division,
                                                  Servicio, Seccion)
from apps.complementos.salud.models import Especialidad
from apps.instituciones.models import Institucion
from apps.personas.models import Persona
# from . import helpers


class SituacionLaboral(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Situacion del Empleado"


class Empleado(models.Model):
    persona = models.OneToOneField(Persona, unique=True)
    cuil = models.CharField(max_length=15, null=True, blank=True)
    cuit = models.CharField(max_length=15, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_egreso = models.DateField(null=True, blank=True)
    situacion_laboral = models.ForeignKey(SituacionLaboral, null=True,
                                          blank=True)

    def __str__(self):
        return str(self.persona)

    class Meta:
        ordering = ["persona__apellido"]
        verbose_name_plural = "Empleados"


class EmpleadoEspecialidad(models.Model):
    especialidad = models.ForeignKey(Especialidad, unique=False)
    empleado = models.ForeignKey(Empleado, unique=False)

    class Meta:
        verbose_name_plural = "Empleado-Especialidad"


class Asignacion(models.Model):
    empleado = models.ForeignKey(
        Empleado, unique=False, null=True, blank=True)
    destino = models.ForeignKey(
        Institucion, unique=False, null=True, blank=True)
    cargo = models.ForeignKey(Cargo, unique=False, null=True, blank=True)
    direccion = models.ForeignKey(
        Direccion, unique=False, null=True, blank=True)
    departamento = models.ForeignKey(
        Departamento, unique=False, null=True, blank=True)
    division = models.ForeignKey(Division, unique=False, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, unique=False, null=True, blank=True)
    seccion = models.ForeignKey(Seccion, unique=False, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    class Meta:
        abstract = True


class AsignacionFormal(Asignacion):
    fecha_desde = models.DateField(null=True, blank=True)
    fecha_hasta = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.destino) + " - " + str(self.cargo)

    class Meta:
        ordering = ['-fecha_hasta']
        verbose_name_plural = "Asignaciones Formales de Empleados"


# class AsignacionActual(AsignacionEmpleado):
#     funcion_triage = models.BooleanField(default=True, blank=True)
#
#
#     def __str__(self):
#         return self.destino
#
#     class Meta:
#         verbose_name_plural = "Asignacion Actual de Empleados"
