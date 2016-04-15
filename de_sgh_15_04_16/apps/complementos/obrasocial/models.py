from django.db import models


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    abreviatura = models.CharField(max_length=20, null=True, blank=True)
    codigo_padron = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Obras Sociales"


class MotivoSuspension(models.Model):
    descripcion = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ['descripcion']
        verbose_name_plural = "Motivos de Suspensiones"
