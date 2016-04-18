# -*- encoding: utf-8 -*-
from datetime import datetime
from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.models import User
from django.db import models

from apps.complementos.obrasocial.models import (ObraSocial, MotivoSuspension)
from apps.complementos.organigrama.models import Profesion
from apps.complementos.paciente.models import Categoria
from apps.complementos.persona.models import (Sexo, TipoDocumento, EstadoCivil,
                                              NivelEducacion, Parentesco, Etnia)


class Persona(models.Model):
    apellido = models.CharField(max_length=30, null=True, blank=True)
    nombre = models.CharField(max_length=30, null=True, blank=True)
    tipo_documento = models.ForeignKey(
        TipoDocumento, null=True, blank=True, default=1)
    numero_documento = models.CharField(
        max_length=20, null=True, blank=True, unique=False)
    sexo = models.ForeignKey(Sexo, null=True, blank=True)
    fecha_nacimiento = models.DateField(default='1900-01-01', null=False)
    estado_civil = models.ForeignKey(EstadoCivil, null=True, blank=True)
    obra_social = models.ForeignKey(ObraSocial, null=True, blank=True)
    foto = models.ImageField(
        upload_to='foto_personal', blank=True, null=True)
    nivel_educacion = models.ForeignKey(NivelEducacion, null=True, blank=True)
    profesion = models.ForeignKey(Profesion, null=True, blank=True)
    etnia = models.ForeignKey(Etnia, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def get_edad(self):
        fecha_actual = datetime.today().date()
        edad = int((fecha_actual - self.fecha_nacimiento).days / 365.25)
        return edad

    def __str__(self):
        return str(self.apellido) + ", " + str(self.nombre)

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(MEDIA_URL, self.foto.url)

    class Meta:
        ordering = ["apellido"]


class UserProfile(models.Model):
    usuario = models.OneToOneField(User)
    persona = models.OneToOneField(Persona)


TIPO_BENEFICIARIO = (('T', 'Titular'), ('A', 'Adherente'), )


class PersonaObraSocial(models.Model):

    persona = models.ForeignKey(Persona, null=True, blank=True)
    obra_social = models.ForeignKey(ObraSocial, default=1)
    numero_afiliado = models.CharField(max_length=20)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    tipo_beneficiario = models.CharField(max_length=1,
                                         choices=TIPO_BENEFICIARIO)
    parentesco = models.ForeignKey(Parentesco, null=True, blank=True)
    categoria = models.ForeignKey(Categoria)
    habitual = models.BooleanField(default=True)
    suspendida = models.BooleanField(default=False)
    motivo_suspension = models.ForeignKey(
        MotivoSuspension, null=True, blank=True)
    observacion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.obra_social)

    class Meta:
        verbose_name_plural = "Personas - Obras Sociales"
