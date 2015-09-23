from django.db import models
from apps.agendas.models import AgendaCalendario
# from apps.complementos.salud.models import Practica
from apps.clientes.models import Cliente


class Turno(models.Model):
    agenda_calendario = models.ForeignKey(
        AgendaCalendario, blank=False, null=False)
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fin = models.TimeField(blank=False, null=False)
    bloqueado = models.BooleanField(default=False, blank=False)
    # practica = models.ForeignKey(Practica, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __str__(self):
        return str(self.hora_desde) + " - " + str(self.hora_hasta)

    class Meta:
        verbose_name_plural = 'Rango Horario'