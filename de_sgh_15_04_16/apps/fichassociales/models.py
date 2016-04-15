from django.db import models

from apps.complementos.IVA.models import TipoIVA
from apps.complementos.locacion.models import (Pais, Provincia, Departamento,
                                               Localidad, Barrio)
from apps.complementos.paciente.models import SituacionLaboral
from apps.pacientes.models import Paciente

# COMPLEMENTOS ASPECTOS HABITACIONALES


class SituacionPropiedad(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Situaciones de la Propiedad"
        verbose_name = "Situación de la Propiedad"


class TipoVivienda(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Viviendas"
        verbose_name = "Tipo de Vivienda"


class TerrenoPropio(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Terrenos Propios"
        verbose_name = "Terreno Propio"


class TipoConstruccion(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Construcciones"
        verbose_name = "Tipo de Construcción"


class ServicioAgua(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Servicios de Agua"
        verbose_name = "Servicio de Agua"


class ServicioLuzElectrica(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Servicios de Luz Electrica"
        verbose_name = "Servicio de Luz Eléctrica"


class OtroServicio(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Otros Servicios"
        verbose_name = "Otro Servicio"


class TipoBanio(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Baños"
        verbose_name = "Tipo de Baño"


class TipoTecho(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Techos"
        verbose_name = "Tipo de Techo"


class TipoPared(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Paredes"
        verbose_name = "Tipo de Pared"


class TipoPiso(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Pisos"
        verbose_name = "Tipo de Piso"


class TipoProgramaSocial(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Programas Sociales"
        verbose_name = "Tipo de Programa Social"


class FichaSocial(models.Model):
    paciente = models.OneToOneField(Paciente)
    numero_ficha = models.CharField(max_length=50, unique=True,
                                    null=True, blank=True)
    ultima_verificacion = models.DateField(null=True, blank=True)

    situacion_laboral = models.ForeignKey(
        SituacionLaboral, null=True, blank=True)

    tipo_iva = models.ForeignKey(TipoIVA, null=True, blank=True)
    # DATOS DE LA EMPRESA
    lugar_trabajo = models.CharField(max_length=50, blank=True, null=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, null=True, blank=True)

    descripcion_domicilio = models.TextField(max_length=None,
                                             null=True, blank=True)

    codigo_postal = models.CharField(max_length=20, null=True, blank=True)

    # ASPECTOS HABITACIONALES
    situacion_propiedad = models.ForeignKey(
        SituacionPropiedad, null=True, blank=True)

    tipo_vivienda = models.ForeignKey(TipoVivienda, null=True, blank=True)
    terreno_propio = models.ForeignKey(TerrenoPropio, null=True, blank=True)

    tipo_construccion = models.ForeignKey(
        TipoConstruccion, null=True, blank=True)

    servicio_agua = models.ForeignKey(ServicioAgua, null=True, blank=True)

    servicio_luz_electrica = models.ForeignKey(
        ServicioLuzElectrica, null=True, blank=True)

    otro_servicio = models.ForeignKey(OtroServicio, null=True, blank=True)
    tipo_banio = models.ForeignKey(TipoBanio, null=True, blank=True)
    tipo_techo = models.ForeignKey(TipoTecho, null=True, blank=True)
    tipo_pared = models.ForeignKey(TipoPared, null=True, blank=True)
    tipo_piso = models.ForeignKey(TipoPiso, null=True, blank=True)
    # CANTIDADES
    cantidad_dormitorio = models.IntegerField(null=True, blank=True)
    cantidad_ambiente = models.IntegerField(null=True, blank=True)
    cantidad_cama = models.IntegerField(null=True, blank=True)
    # PROGRAMAS SOCIALES
    programa_social = models.ManyToManyField(
        TipoProgramaSocial, blank=True)

    observacion_socio_economica = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.numero_ficha) + ' - ' + str(self.paciente)

    class Meta:
        verbose_name_plural = "Fichas Sociales"
        verbose_name = "Ficha Social"

# Create your models here.
