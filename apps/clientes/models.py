from django.db import models

from apps.personas.models import Persona


class SituacionLaboral(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Situacion Laboral"


class Cliente(models.Model):
    persona = models.OneToOneField(Persona, unique=True, blank=True)
    cuil = models.CharField(max_length=15, null=True, blank=True)
    fecha_alta_sistema = models.DateTimeField(auto_now_add=True)
    situacion_laboral = models.ForeignKey(SituacionLaboral, null=True,
                                          blank=True)

    def __str__(self):
        return str(self.persona)

    class Meta:
        verbose_name_plural = "Clientes"