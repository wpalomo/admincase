from django.db import models


class Sexo(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    abreviatura = models.CharField(max_length=1, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Tipos de Sexo"


class TipoDocumento(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.abreviatura.upper()

    class Meta:
        verbose_name_plural = "Tipos de Documentos"


class EstadoCivil(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Estados Civiles"


class NivelEducacion(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Nivel  de Educacion"