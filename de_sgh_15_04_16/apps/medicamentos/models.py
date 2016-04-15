from django.db import models

from apps.complementos.salud.models import UnidadMedida


class PrincipioActivo(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Principios Activos"


class LineaTerapeutica(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Lineas Terapeuticas"


class ViaAdministracion(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Vias de Administracion"


class FormaFarmaceutica(models.Model):
    via_administracion = models.ForeignKey(
        ViaAdministracion, unique=False, null=True, blank=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Tipos de Formas Farmaceuticas"


class Catalogo(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Catalogos"


class NumeroAutoincremental(models.Model):
    numero = models.IntegerField()
    tipo = models.OneToOneField(Catalogo, null=False, blank=True)

    def __str__(self):
        return str(self.numero) + ' || ' + str(self.tipo)

    class Meta:
        verbose_name_plural = "Numero Autoincremental"


# PARA MEDICAMENTO - LABORATORIO

class Laboratorio(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Laboratorios"


class Envase(models.Model):

    """ Contiene los tipos de envases de los medicamentos """

    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Envase'
        verbose_name_plural = 'Envases'


class Agrupado(models.Model):

    """ Contiene los envases de las presentaciones de los medicamentos """

    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Agrupados"


class Pack(models.Model):

    """ Contiene los agrupados de los medicamentos """

    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Packs de Unidades de Despachos"


class Pallet(models.Model):

    """ Contiene los packs de los agrupados """

    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Pallet de Unidades Logisticas"

# FIN MEDICAMENTO - LABORATORIO


class Medicamento(models.Model):
    catalogo = models.ForeignKey(Catalogo, unique=False, null=True, blank=True)
    codigo = models.IntegerField(null=True, blank=True)
    denominacion = models.CharField(max_length=100)
    producto_combinado = models.BooleanField(default=False)
    libre_azucar = models.BooleanField(default=False)
    libre_conservante = models.BooleanField(default=False)
    libre_cfc = models.BooleanField(default=False)
    libre_gluten = models.BooleanField(default=False)

    def __str__(self):
        return str(self.codigo) + ' || ' + self.denominacion

    def get_codigo(self):
        return str(self.codigo).zfill(10)

    class Meta:
        verbose_name_plural = "Medicamentos"


class Composicion(models.Model):
    medicamento = models.ForeignKey(Medicamento, unique=False, blank=True)
    principio_activo = models.ForeignKey(
        PrincipioActivo, unique=False, null=True, blank=True)
    potencia_numerador = models.IntegerField(null=True, blank=True)
    unidad_medida_numerador = models.ForeignKey(
        UnidadMedida, unique=False, null=True, blank=True,
        related_name="unidad_medida_numerador")
    potencia_denominador = models.IntegerField(null=True, blank=True)
    unidad_medida_denominador = models.ForeignKey(
        UnidadMedida, unique=False, null=True, blank=True,
        related_name="unidad_medida_denominador")

    def __str__(self):
        return str(self.medicamento)

    class Meta:
        verbose_name_plural = "Composicion de Medicamentos"


class MedicamentoLineaTerapeutica(models.Model):
    medicamento = models.ForeignKey(
        Medicamento, unique=False, null=True, blank=True)
    linea_terapeutica = models.ForeignKey(
        LineaTerapeutica, unique=False, null=True, blank=True)

    def __str__(self):
        return str(self.linea_terapeutica)

    class Meta:
        verbose_name_plural = "Lineas Terapeuticas"


class AdministracionForma(models.Model):
    medicamento = models.ForeignKey(
        Medicamento, unique=False, null=True, blank=True)
    via_administracion = models.ForeignKey(
        ViaAdministracion, unique=False, null=True, blank=True)
    forma_farmaceutica = models.ForeignKey(
        FormaFarmaceutica, unique=False, null=True, blank=True)

    def __str__(self):
        return str(self.medicamento) + ' || ' + str(self.via_administracion) + \
            ' || ' + str(self.forma_farmaceutica)

    class Meta:
        verbose_name_plural = "Administracion y Formas"


class MedicamentoLaboratorio(models.Model):
    medicamento = models.ForeignKey(
        Medicamento, unique=False, null=True, blank=True)
    nombre_comercial = models.CharField(max_length=100)
    laboratorio = models.ForeignKey(
        Laboratorio, unique=False, null=True, blank=True)
    numero_certificado = models.IntegerField(null=True, blank=True)
    numero_gtin = models.CharField(max_length=40, null=True, blank=True)
    forma_farmaceutica = models.ForeignKey(
        FormaFarmaceutica, unique=False, null=True, blank=True)
    envase_primario = models.ForeignKey(
        Envase, unique=False, null=True, blank=True,
        related_name="envase_primario")
    cantidad_envase_primario = models.IntegerField(null=True, blank=True)
    unidad_medida_envase_primario = models.ForeignKey(
        UnidadMedida, unique=False, null=True, blank=True,
        related_name="unidad_medida_envase_primario")
    envase_secundario = models.ForeignKey(
        Envase, unique=False, null=True, blank=True,
        related_name="envase_secundario")
    cantidad_envase_secundario = models.IntegerField(null=True, blank=True)
    unidad_medida_envase_secundario = models.ForeignKey(
        UnidadMedida, unique=False, null=True, blank=True,
        related_name="unidad_medida_envase_secundario")

    agrupado_cantidad = models.IntegerField(null=True, blank=True)
    agrupado_unidad = models.ForeignKey(
        Agrupado, null=True, blank=True)

    pack_cantidad = models.IntegerField(null=True, blank=True)
    pack_unidad_despacho = models.ForeignKey(
        Pack, null=True, blank=True)

    pallet_cantidad = models.IntegerField(null=True, blank=True)
    pallet_unidad_logistica = models.ForeignKey(
        Pallet, null=True, blank=True)
    imagen_medicamento = models.ImageField(upload_to='imagen_medicamento',
                                           null=True, blank=True)
    prospecto_medicamento = models.FileField(upload_to='prospecto_medicamento',
                                             null=True, blank=True)

    class Meta:
        verbose_name_plural = "Medicamento - Laboratorios"

    def __str__(self):
        return str(self.medicamento) + ' || ' + str(self.laboratorio)
