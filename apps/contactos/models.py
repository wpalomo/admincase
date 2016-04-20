
from django.db import models

from apps.personas.models import Persona


class TipoContacto(models.Model):

    descripcion = models.CharField(max_length=100, null=False, blank=False)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Tipo de contacto'
        verbose_name_plural = 'Tipos de contactos'


class Contacto(models.Model):

    persona = models.ForeignKey(Persona, null=False, blank=False)
    proveedor = models.CharField(max_length=100,
                                 null=True, blank=True)
    tipo_contacto = models.ForeignKey(TipoContacto, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    observacion = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.persona.nombre) + '-' + str(self.persona.apellido) \
               + " - " + self.descripcion

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
