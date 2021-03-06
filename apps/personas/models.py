# -*- encoding: utf-8 -*-
import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from apps.complementos.persona.models import (Sexo, TipoDocumento,
                                              EstadoCivil, NivelEducacion)
from apps.complementos.organigrama.models import Profesion
from apps.complementos.salud.models import ObraSocial


def _generar_ruta_imagen(instance, filename):
        # El primer paso es extraer la extension de la imagen del
        # archivo original
        extension = os.path.splitext(filename)[1][1:]

        # Generamos la ruta relativa a MEDIA_ROOT donde almacenar
        # el archivo, usando la fecha actual (año/mes)
        # ruta = os.path.join('foto_persona', date.today().strftime("%Y/%m"))
        # ruta = os.path.join('foto_persona')
        ruta = 'foto_persona'

        # Generamos el nombre del archivo con un identificador
        # aleatorio, y la extension del archivo original.
        nombre_archivo = '{}.{}'.format(instance.numero_documento, extension)

        # Devolvermos la ruta completa
        return os.path.join(ruta, nombre_archivo)


class Persona(models.Model):
    foto = models.ImageField(upload_to=_generar_ruta_imagen, blank=True,
                             null=True)
    apellido = models.CharField(max_length=30, null=True, blank=True)
    nombre = models.CharField(max_length=30, null=True, blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, null=False, blank=False,
                                       default=1)
    numero_documento = models.CharField(max_length=20, null=True, blank=True,
                                        unique=False)
    sexo = models.ForeignKey(Sexo, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=False)
    estado_civil = models.ForeignKey(EstadoCivil, null=True, blank=True)
    obra_social = models.ForeignKey(ObraSocial, null=True, blank=True)
    nivel_educacion = models.ForeignKey(NivelEducacion, null=True, blank=True)
    profesion = models.ForeignKey(Profesion, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.apellido) + ", " + str(self.nombre)

    def edad(self):
        #CALCULO DE EDAD
        if self.fecha_nacimiento:
            fecha_nacimiento_persona = datetime.strptime(str(self.fecha_nacimiento), "%Y-%m-%d").date()
            f_actual = datetime.today().date()
            anios = int((f_actual - fecha_nacimiento_persona).days / 365.25)
            meses = int(((f_actual - fecha_nacimiento_persona).days / 365.25 - anios) * 12)
            dias = int((((f_actual - fecha_nacimiento_persona).days / 365.25 - anios) * 12 - meses) * 30)
            edad = str(anios) + " años, " + str(meses) + " meses y " + str(dias) + " días"
        else:
            edad = ""
        return str(edad)


class UserProfile(models.Model):
    usuario = models.OneToOneField(User)
    persona = models.OneToOneField(Persona)
