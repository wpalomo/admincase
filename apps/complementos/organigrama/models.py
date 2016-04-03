import os
from django.db import models


class Profesion(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    #audit_log = AuditLog()

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Profesiones"
        ordering = ['nombre']


def _generar_ruta_imagen(instance, filename):
        # El primer paso es extraer la extension de la imagen del
        # archivo original
        extension = os.path.splitext(filename)[1][1:]

        # Generamos la ruta relativa a MEDIA_ROOT donde almacenar
        # el archivo, usando la fecha actual (año/mes)
        # ruta = os.path.join('foto_persona', date.today().strftime("%Y/%m"))
        # ruta = os.path.join('foto_persona')
        ruta = 'logo/tramites_entidades'

        # Generamos el nombre del archivo con un identificador
        # aleatorio, y la extension del archivo original.
        nombre_archivo = '{}.{}'.format(instance.nombre, extension)

        # Devolvermos la ruta completa
        return os.path.join(ruta, nombre_archivo)


class Entidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False)
    imagen = models.ImageField(
        upload_to=_generar_ruta_imagen, blank=True, null=True)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Entidades"
        ordering = ['nombre']