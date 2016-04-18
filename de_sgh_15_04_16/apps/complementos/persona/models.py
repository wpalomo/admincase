from django.db import models


class Sexo(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    abreviatura = models.CharField(max_length=1, null=True, blank=True)
    # audit_log = AuditLog()

    def __str__(self):
        return str(self.descripcion)

    class Meta:
        verbose_name_plural = "Tipos de Sexo"


class TipoDocumento(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)
    longitud = models.IntegerField()
    # audit_log = AuditLog()

    def __str__(self):
        return str(self.abreviatura)

    class Meta:
        verbose_name_plural = "Tipos de Documentos"


class EstadoCivil(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)
    # audit_log = AuditLog()

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Estados Civiles"


class NivelEducacion(models.Model):
    descripcion = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)
    # audit_log = AuditLog()

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Nivel  de Educacion"


class Parentesco(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    abreviatura = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Parentesco"


class Etnia(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Etnias"
