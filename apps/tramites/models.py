from django.db import models

from apps.complementos.organigrama.models import Entidad
from apps.personas.models import Persona


class Requisito(models.Model):
<<<<<<< HEAD
    nombre = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.nombre
=======
    descripcion = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.descripcion
>>>>>>> e7fa682023eb99d4c44cc902feea95cf2b0a235f

    class Meta:
        verbose_name_plural = "Requisitos de Tramite"


class TipoTramite(models.Model):
<<<<<<< HEAD
    nombre = models.CharField(max_length=30)
=======
    descripcion = models.CharField(max_length=30)
>>>>>>> e7fa682023eb99d4c44cc902feea95cf2b0a235f
    entidad = models.ForeignKey(Entidad)
    requisitos = models.ManyToManyField(Requisito)

    def __str__(self):
<<<<<<< HEAD
        return self.nombre + ' - ' + str(self.entidad)
=======
        return self.descripcion
>>>>>>> e7fa682023eb99d4c44cc902feea95cf2b0a235f

    class Meta:
        verbose_name_plural = "Tipos de Tramite"


class Tramite(models.Model):
    persona = models.ForeignKey(Persona)
    tipo = models.ForeignKey(TipoTramite, unique=True)
    estado = models.BooleanField(default=False, blank=True)
    observaciones = models(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.tipo)

    class Meta:
        verbose_name_plural = "Tramites"


class RequisitoPresentado(models.Model):
<<<<<<< HEAD
    tramite = models.ForeignKey(TipoTramite, null=True, blank=True)
=======
    tramite = models.ForeignKey(Tramite, null=True, blank=True)
>>>>>>> e7fa682023eb99d4c44cc902feea95cf2b0a235f
    requisito = models.ForeignKey(Requisito, null=True, blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
<<<<<<< HEAD
        return str(self.tramite) + '-' + str(self.requisito) + '-' + str(self.estado)



=======
        return str(self.tramite) + '-' + str(self.requisito) + '-' + str(self.estado)
>>>>>>> e7fa682023eb99d4c44cc902feea95cf2b0a235f
