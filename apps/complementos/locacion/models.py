from django.db import models


class Pais(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)

    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Paises"


class Provincia(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    pais = models.ForeignKey(Pais)

    # audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Provincias"


class Departamento(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    provincias = models.ForeignKey(Provincia)

    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Departamentos"


class Localidad(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    departamentos = models.ForeignKey(Departamento, null=True, blank=True)

    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Localidades"


# class Barrio(models.Model):
#
#     nombre = models.CharField(max_length=50, null=True, blank=True)
#     descripcion = models.CharField(max_length=500, null=True, blank=True)
#     localidades = models.ForeignKey(Localidad, null=True, blank=True)
#
#     #audit_log = AuditLog()
#
#     def __str__(self):
#         return self.nombre.title()
#
#     class Meta:
#         verbose_name_plural = "Barrios"
