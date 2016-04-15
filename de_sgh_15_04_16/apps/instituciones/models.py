
from django.db import models

from apps.complementos.locacion.models import Pais, Provincia, Departamento


class Institucion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    cuit = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    pais = models.ForeignKey(Pais)
    provincia = models.ForeignKey(Provincia)
    departamento = models.ForeignKey(Departamento)
    domicilio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

    def codigo(self):
        return str(self.id).zfill(4)

    class Meta:
        verbose_name_plural = "Instituciones"
