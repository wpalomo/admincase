# -*- coding: utf-8 -*-

from django.db import models


class ArbolItem(models.Model):

    descripcion = models.CharField(max_length=100)
    link = models.CharField(max_length=100, null=True, blank=True)
    padre_id = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    is_folder = models.BooleanField(default=True)
    modulo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Modulos ArbolItem"