
from django.db import models

from apps.complementos.salud.models import Especialidad, Practica
from apps.empleados.models import Empleado
from apps.instituciones.models import Institucion


class Dia(models.Model):
    nombre = models.CharField(max_length=20)
    numero = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Dias de la semana'


class MotivoBloqueo(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Motivo de Bloqueo'


class TipoAgenda(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = 'Tipos de Agenda'


class Agenda(models.Model):
    institucion = models.ForeignKey(Institucion, unique=False)
    profesional = models.ForeignKey(Empleado, unique=False)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    especialidad = models.ForeignKey(Especialidad, unique=False)
    tipo_agenda = models.ForeignKey(TipoAgenda, unique=False)

    def __str__(self):
        return str(self.institucion) + ' - ' + str(self.tipo_agenda)

    class Meta:
        verbose_name_plural = 'Agenda'


class AgendaPeriodoBloqueo(models.Model):
    agenda = models.ForeignKey(Agenda, unique=False)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    motivo_bloqueo = models.ForeignKey(MotivoBloqueo, unique=False)
    observacion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Agenda Bloqueos'


class AgendaDiaConfiguracion(models.Model):
    agenda = models.ForeignKey(Agenda, unique=False)
    dia = models.ForeignKey(Dia, unique=False)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    hora_desde = models.TimeField()
    hora_hasta = models.TimeField()
    duracion_minutos = models.IntegerField(default=0)
    practica = models.ForeignKey(Practica, unique=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Configuracion Dias de Agenda'


class AgendaDiaConfiguracionBloqueo(models.Model):
    agenda = models.ForeignKey(Agenda, unique=False)
    dia_configuracion = models.ForeignKey(AgendaDiaConfiguracion, unique=False)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    motivo_bloqueo = models.ForeignKey(MotivoBloqueo, unique=False)
    observacion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Agenda Dia Bloqueos'


class AgendaFechaDetalle(models.Model):
    agenda = models.ForeignKey(Agenda, unique=False)
    dia_configuracion = models.ForeignKey(AgendaDiaConfiguracion, unique=False)
    fecha = models.DateField()
    hora_desde = models.TimeField()
    hora_hasta = models.TimeField()
    duracion_minutos = models.IntegerField(default=0)
    practica = models.ForeignKey(Practica, unique=False, null=True, blank=True)

    def __str__(self):
        practica = self.practica if self.practica else 'Consulta'
        texto = str(self.fecha) + ' (' + str(practica) + ' | '
        texto += str(self.hora_desde) + ' - ' + str(self.hora_hasta)
        texto += ')'

        return texto

    class Meta:
        verbose_name_plural = 'Detalle Agenda por Fecha'


class AgendaFechaDetalleBloqueo(models.Model):
    agenda = models.ForeignKey(Agenda, unique=False, null=True)
    dia_configuracion = models.ForeignKey(
        AgendaDiaConfiguracion, unique=False, null=True)
    fecha_detalle = models.ForeignKey(AgendaFechaDetalle, unique=False)
    motivo_bloqueo = models.ForeignKey(MotivoBloqueo, unique=False)
    observacion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Agenda Fecha Detalle Bloqueos'