from django.db import models
from django.contrib.auth.models import User
from apps.personas.models import Persona


class TipoNota(models.Model):

    descripcion = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Tipo de Nota'
        verbose_name_plural = 'Tipos de Notas'


class Nota(models.Model):

    persona = models.ForeignKey(Persona, null=False, blank=False)
    fecha = models.DateField(auto_now=True, null=False, blank=False)
    hora = models.TimeField(auto_now=True, null=False, blank=False)
    tipo_nota = models.ForeignKey(TipoNota, null=False, blank=False)
    descripcion = models.TextField(max_length=3000, null=False, blank=False)
    usuario = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return str(self.tipo_nota) + " - " + str(self.descripcion)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
