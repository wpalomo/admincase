# -*- coding: utf-8 -*-
from django.db import models

'''
class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    abreviatura = models.CharField(max_length=20, null=True, blank=True)
    codigo_padron = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Obras Sociales"
'''


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Especialidades"


class Practica(models.Model):
    especialidad = models.ForeignKey(Especialidad, unique=False)
    nombre = models.CharField(max_length=100, unique=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Practicas"


class GrupoSanguineo(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Grupo Sanguineo"


class UnidadMedida(models.Model):
    descripcion = models.CharField(max_length=20, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Unidades de Medidas"
        ordering = ['descripcion']
