from django.db import models


class Categoria(models.Model):
    descripcion = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        ordering = ['descripcion']
        verbose_name_plural = "Categorias"


class SituacionLaboral(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Situacion Laboral"
        verbose_name_plural = "Situaciones Laborales"
