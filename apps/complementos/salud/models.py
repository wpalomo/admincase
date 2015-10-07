# -*- coding: utf-8 -*-
from django.db import models


class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    abreviatura = models.CharField(max_length=10, null=True, blank=True)
    codigo_padron = models.IntegerField()
    #audit_log = AuditLog()

    def __str__(self):
        return self.abreviatura.upper()

    class Meta:
        verbose_name_plural = "Obras Sociales"


class GrupoSanguineo(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.abreviatura.upper()

    class Meta:
        verbose_name_plural = "Grupos Sanguineos"