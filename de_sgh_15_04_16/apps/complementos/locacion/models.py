from django.db import models

# from apps.personas.models import Persona


class Pais(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Paises"


class Provincia(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    pais = models.ForeignKey(Pais)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Provincias"


class Departamento(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    provincia = models.ForeignKey(Provincia)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Departamentos"


class Localidad(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Localidades"


class Barrio(models.Model):

    nombre = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)

    def __str__(self):
        return self.nombre.title()

    class Meta:
        verbose_name_plural = "Barrios"


class LugarNacimiento(models.Model):
    pass
    # para alan

    # persona = models.OneToOneField(Persona, unique=True)
    # pais = models.ForeignKey(Pais, null=False, blank=False)
    # provincia = models.ForeignKey(Provincia, null=True, blank=True)
    # departamento = models.ForeignKey(Departamento, null=True, blank=True)
    #
    # def __str__(self):
    #     return '%s, %s - %s, %s, %s' % (
    #         self.persona.nombre, self.persona.apellido, self.pais,
    #         self.provincia, self.departamento)
    #
    # class Meta:
    #     verbose_name = 'Lugar de nacimiento'
    #     verbose_name_plural = 'Lugares de Nacimientos'
