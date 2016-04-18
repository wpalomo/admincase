# -*- encoding: utf-8 -*-
from django.db import models
from apps.complementos.salud.models import GrupoSanguineo
from apps.personas.models import Persona


class TipoPaciente(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)
    valor = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.descripcion.title())

    class Meta:
        verbose_name_plural = "Tipos de Pacientes"


class Clase(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return str(self.descripcion.title())

    class Meta:
        verbose_name_plural = "Clases de Pacientes"


class Paciente(models.Model):
    persona = models.OneToOneField(Persona, unique=True)
    cuil = models.CharField(max_length=15, null=True, blank=True)
    cuit = models.CharField(max_length=80, null=True, blank=True)
    tipo = models.ForeignKey(TipoPaciente, null=False)
    clase = models.ForeignKey(Clase, null=True, blank=True)
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, null=True, blank=True)
    fecha_alta_sistema = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' % (str(self.persona.nombre), str(self.persona.apellido))

    class Meta:
        verbose_name_plural = "Pacientes"
