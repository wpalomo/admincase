from django.db import models

from apps.personas.models import Persona
from apps.pacientes.models import Paciente
from apps.complementos.persona.models import Parentesco


class Ocupacion(models.Model):

    descripcion = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Ocupacion'
        verbose_name_plural = 'Ocupaciones'


class SituacionLaboral(models.Model):

    descripcion = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Situacion laboral'
        verbose_name_plural = 'Situaciones laborales'


class TipoRelacion(models.Model):

    descripcion = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Tipo de relacion'
        verbose_name_plural = 'Tipos de relaciones'


class Familiar(models.Model):

    persona = models.OneToOneField(Persona, unique=True)
    vive = models.BooleanField(default=True)
    motivo_fallecimiento = models.TextField(max_length=600, null=True,
                                            blank=True)
    ocupacion = models.ForeignKey(Ocupacion, null=True, blank=True)
    situacion_laboral = models.ForeignKey(SituacionLaboral,
                                          null=True, blank=True)
    otra_ayuda_economica = models.CharField(max_length=60, null=True,
                                            blank=True)
    economicamente_activo = models.BooleanField(default=False)

    def __str__(self):
        return '%s, %s' % (self.persona.nombre, self.persona.apellido)

    class Meta:
        verbose_name = 'Familiar'
        verbose_name_plural = 'Familiares'


class FamiliarPaciente(models.Model):

    familiar = models.ForeignKey(Familiar, null=False, blank=False)
    paciente = models.ForeignKey(Paciente, null=False, blank=False)
    parentesco = models.ForeignKey(Parentesco, null=False, blank=False)
    tipo_relacion = models.ForeignKey(TipoRelacion, null=True, blank=True)
    responsable = models.BooleanField(default=False)
    convive_misma_vivienda = models.BooleanField(default=False)
    observacion = models.TextField(max_length=600, null=True, blank=True)

    def __str__(self):
        return '%s, %s %s DE %s, %s' % (str(self.familiar.persona.nombre).upper(),
                                        str(self.familiar.persona.apellido).upper(),
                                        self.parentesco,
                                        self.paciente.persona.nombre,
                                        self.paciente.persona.apellido)

    class Meta:
        verbose_name = 'Familiar y paciente'
        verbose_name_plural = 'Familiares y pacientes'

