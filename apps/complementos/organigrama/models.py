from django.db import models


class Profesion(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Profesiones"
        ordering = ['nombre']


class Entidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False)
    # requisitos = models.CharField

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Entidades"
        ordering = ['nombre']