from django.db import models

from apps.empleados.models import Empleado
from apps.proveedores.models import Proveedor


class ServicioAdministracion(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class TipoResolucion(models.Model):
    descripcion = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class NumeroAutoincremental(models.Model):
    numero = models.IntegerField()
    tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.numero) + ' || ' + self.tipo


class Clase(models.Model):
    descripcion = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion.title()


class Estado(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Estado Expedientes"


class Etapa(models.Model):
    descripcion = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    resolucion = models.IntegerField(default=0)
    disposicion = models.IntegerField(default=0)
    licitacion = models.IntegerField(default=0)
    comodato = models.IntegerField(default=0)
    servicio_medico = models.IntegerField(default=0)
    resoluciones_varias = models.IntegerField(default=0)
    resolucion_contratacion = models.IntegerField(default=0)

    def __str__(self):
        return self.descripcion


class FuenteFinanciamiento(models.Model):
    cuenta = models.CharField(max_length=100)
    fondo = models.CharField(max_length=100)

    def __str__(self):
        return self.cuenta + ' || ' + self.fondo


class Expediente(models.Model):
    letra = models.CharField(max_length=1, null=True, blank=True)
    numero = models.CharField(max_length=15, null=True, blank=True)
    anio = models.CharField(max_length=2, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    clase = models.ForeignKey(Clase, unique=False, null=True, blank=True)
    tipo_resolucion = models.ForeignKey(
        TipoResolucion, unique=False, null=True, blank=True)
    estado = models.ForeignKey(Estado, unique=False, null=True, blank=True)
    empleado_solicitante = models.ForeignKey(
        Empleado, unique=False, related_name='empleado_solicitante',
        null=True, blank=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    etapa = models.ForeignKey(Etapa, unique=False, null=True, blank=True)

    def __str__(self):
        return str(self.letra) + '-' + str(self.numero).zfill(4) + '-' + \
               str(self.anio)

    class Meta:
        ordering = ['-fecha', '-numero', '-anio']
        verbose_name_plural = "Expediente"


class ExpedienteResolucion(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    caja_chica = models.CharField(
        default=0, max_length=1, null=True, blank=True)
    resolucion_adjudicacion = models.CharField(
        max_length=4, null=True, blank=True)
    fecha_resolucion_adjudicacion = models.DateField(null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    importe = models.FloatField(null=True, blank=True)
    tipo_transaccion = models.CharField(max_length=100, null=True, blank=True)
    numero_identificacion_transaccion = models.CharField(
        max_length=4, null=True, blank=True)
    orden_provision = models.CharField(max_length=4, null=True, blank=True)
    acta_recepcion = models.CharField(max_length=4, null=True, blank=True)
    fuente_financiamiento = models.ForeignKey(
        FuenteFinanciamiento, unique=False, null=True, blank=True)
    numero_resolucion_pago = models.CharField(
        max_length=4, null=True, blank=True)
    fecha_resolucion_pago = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Resolucion"


class ExpedienteDisposicion(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    contratacion_directa = models.IntegerField(null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    importe = models.FloatField(null=True, blank=True)
    numero_disposicion = models.IntegerField(null=True, blank=True)
    fecha_disposicion = models.DateField(null=True, blank=True)
    fuente_financiamiento = models.ForeignKey(
        FuenteFinanciamiento, unique=False, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Disposicion"


class ExpedienteServicioMedico(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    servicio_administracion = models.ForeignKey(
        ServicioAdministracion, unique=False, null=True, blank=True)
    profesional = models.ForeignKey(Empleado, unique=False,
        related_name='profesional', null=True, blank=True)
    resolucion_contratacion = models.CharField(
        max_length=100, null=True, blank=True)
    numero_contratacion = models.CharField(
        max_length=100, null=True, blank=True)
    fecha_resolucion_contratacion = models.DateField(null=True, blank=True)
    orden_provision = models.IntegerField(null=True, blank=True)
    acta_recepcion = models.IntegerField(null=True, blank=True)
    numero_resolucion_pago = models.IntegerField(null=True, blank=True)
    fecha_resolucion_pago = models.DateField(null=True, blank=True)
    importe = models.FloatField(null=True, blank=True)
    tipo_transaccion = models.CharField(max_length=100, null=True, blank=True)
    numero_identificacion_transaccion = models.CharField(
        max_length=4, null=True, blank=True)
    solicitante_resolucion_pago = models.ForeignKey(
        Empleado, unique=False, null=True, blank=True)
    fuente_financiamiento = models.ForeignKey(
        FuenteFinanciamiento, unique=False, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Servicios Medicos"


class ExpedienteLicitacion(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    numero_disposicion = models.IntegerField(null=True, blank=True)
    resolucion_aprobacion = models.CharField(
        max_length=100, null=True, blank=True)
    fecha_resolucion_aprobacion = models.DateField(null=True, blank=True)
    resolucion_adjudicacion = models.CharField(
        max_length=4, null=True, blank=True)
    fecha_resolucion_adjudicacion = models.DateField(null=True, blank=True)
    fuente_financiamiento = models.ForeignKey(
        FuenteFinanciamiento, unique=False, null=True, blank=True)

    def __str__(self):
        return str(self.expediente)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Licitacion"


class ExpedienteLicitacionCompromiso(models.Model):
    expediente_licitacion = models.ForeignKey(
        ExpedienteLicitacion, unique=False, null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    monto_total = models.FloatField(null=True, blank=True)
    orden_provision = models.IntegerField(null=True, blank=True)
    acta_recepcion = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.expediente_licitacion)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Licitacion - Etapa: Compromiso"


class ExpedienteLicitacionOrdenado(models.Model):
    expediente_licitacion = models.ForeignKey(
        ExpedienteLicitacion, unique=False, null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    monto_total = models.FloatField(null=True, blank=True)
    orden_provision = models.IntegerField(null=True, blank=True)
    acta_recepcion = models.IntegerField(null=True, blank=True)

    numero_resolucion_pago = models.IntegerField(null=True, blank=True)
    fecha_resolucion_pago = models.DateField(null=True, blank=True)
    solicitante_resolucion_pago = models.ForeignKey(
        Empleado, unique=False, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.expediente_licitacion.expediente.id)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Licitacion - Etapa: Ordenado"


class ExpedienteComodato(models.Model):
    expediente = models.ForeignKey(Expediente, unique=False)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    resolucion_contratacion = models.CharField(
        null=True, blank=True, max_length=100)
    fecha_resolucion_contratacion = models.DateField(null=True, blank=True)
    numero_contratacion_directa = models.IntegerField(null=True, blank=True)
    importe = models.FloatField(null=True, blank=True)
    orden_provision = models.IntegerField(null=True, blank=True)
    resolucion_pago = models.IntegerField(null=True, blank=True)
    fecha_resolucion_pago = models.DateField(null=True, blank=True)
    solicitante_resolucion_pago = models.ForeignKey(
        Empleado, unique=False, null=True, blank=True)
    fuente_financiamiento = models.ForeignKey(
        FuenteFinanciamiento, unique=False, null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def get_resolucion_pago(self):
        return str(self.resolucion_pago).zfill(4)

    def __str__(self):
        return str(self.expediente)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Comodato"


class ExpedienteResolucionesVarias(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    resolucion_pago = models.IntegerField(null=True, blank=True)
    fecha_resolucion_pago = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    def __str__(self):
        return str(self.expediente)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Resoluciones Varias"


class ExpedienteResolucionContratacion(models.Model):
    expediente = models.OneToOneField(Expediente, unique=False, blank=True)
    proveedor = models.ForeignKey(
        Proveedor, unique=False, null=True, blank=True)
    numero_resolucion = models.IntegerField(null=True, blank=True)
    fecha_resolucion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(max_length=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tipo Expediente: Resolucion Contratacion"