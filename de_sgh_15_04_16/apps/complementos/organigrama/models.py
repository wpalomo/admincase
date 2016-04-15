from django.db import models

from apps.instituciones.models import Institucion


class Cargo(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Cargos de la Institucion"


class Direccion(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Direcciones de la Institucion"


class Departamento(models.Model):
    direccion = models.ForeignKey(Direccion, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Departamentos de la Institucion"


class Division(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Divisiones de la Institucion"


class Servicio(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Servicios de la Institucion"


class Seccion(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True)
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Secciones de la Institucion"


class Profesion(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Profesiones"
        ordering = ['nombre']
