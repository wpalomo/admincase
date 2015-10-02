from django.db import models

class Requisito(models.Model):
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.descripcion

class Entidad(models.Model):
    descripcion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.descripcion

class TipoTramite(models.Model):
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    entidad = models.ForeignKey(Entidad, null=True, blank=True)
    requisitos = models.ManyToManyField(Requisito)

    def __str__(self):
        return self.descripcion

class Tramite(models.Model):
    tipo_tramite = models.ForeignKey(TipoTramite, null=True, blank=True)

    def __str__(self):
        return str(self.tipo_tramite)

class RequisitosPresentados(models.Model):
    tramite = models.ForeignKey(TipoTramite, null=True, blank=True)
    requisito = models.ForeignKey(Requisito, null=True, blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tramite) + '-' + str(self.requisito) + '-' + str(self.estado)



