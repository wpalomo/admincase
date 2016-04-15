
from django.db import models


class Proveedor(models.Model):

    razon_social = models.CharField(max_length=100)
    exclusivo_administracion = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.razon_social