#
# from datetime import datetime
#
# from django.db import models
#
# # from apps.complementos.organigrama.models import Especialidad
# from apps.empleados.models import Empleado
#
#
# class MotivoBloqueo(models.Model):
#     descripcion = models.CharField(max_length=50, blank=False, null=False)
#
#     def __str__(self):
#         return self.descripcion
#
#
# class TipoAgenda(models.Model):
#     descripcion = models.CharField(max_length=50, blank=False, null=False)
#
#     def __str__(self):
#         return self.descripcion
#
#     class Meta:
#         verbose_name_plural = 'Tipos de Agenda'
#
#
# class Agenda(models.Model):
#
#     empleado = models.ForeignKey(Empleado, blank=False, null=False)
#     fecha_desde = models.DateField(
#         default=datetime.now, blank=False, null=False)
#     fecha_hasta = models.DateField(blank=False, null=False)
#     habilitado = models.BooleanField(default=True, blank=False)
#     tipo_agenda = models.ForeignKey(TipoAgenda, blank=False, null=False)
#     # especialidad = models.ForeignKey(Especialidad, blank=False, null=False)
#     bloqueado = models.BooleanField(default=False, blank=False)
#
#     def __str__(self):
#         return str(self.fecha_desde) + " - " + str(self.fecha_hasta)
#
#     class Meta:
#         verbose_name_plural = 'Agenda del Empleado'
#
#
# class AgendaCalendario(models.Model):
#
#     agenda = models.ForeignKey(Agenda, blank=False, null=True)
#     fecha = models.DateField(blank=False, null=False)
#     hora_desde = models.TimeField(blank=False, null=True)
#     hora_hasta = models.TimeField(blank=False, null=True)
#     duracion_minuto = models.IntegerField(blank=False, null=True)
#     cantidad_sobreturnos = models.IntegerField(blank=False, null=True)
#     bloqueado = models.BooleanField(default=False, blank=False)
#
#     def __str__(self):
#         return str(self.agenda)
#
#     class Meta:
#         verbose_name_plural = 'Dias de la Agenda'