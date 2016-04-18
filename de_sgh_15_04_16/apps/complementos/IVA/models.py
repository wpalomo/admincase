from django.db import models


class TipoIVA(models.Model):
    descripcion = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Tipo de IVA"
        verbose_name_plural = "Tipos de IVA"
