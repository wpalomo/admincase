# -*- coding: utf-8 -*-

import time

from datetime import datetime

from django import forms

from apps.empleados.models import Empleado
from apps.proveedores.models import Proveedor

from . import helpers
from .models import (Expediente, ExpedienteResolucion, ExpedienteDisposicion,
                     ExpedienteServicioMedico, ExpedienteLicitacion, Estado,
                     Etapa, Clase, FuenteFinanciamiento, ExpedienteComodato,
                     TipoResolucion, ExpedienteResolucionesVarias,
                     ExpedienteResolucionContratacion,
                     ServicioAdministracion)


LETRAS = (('A', 'A'), ('C', 'C'), ('G', 'G'),
          ('H', 'H'), ('P', 'P'), ('S', 'S'),
          ('-', '-'),)

IMPORTE_MAXIMO_TRANSACCION_DISPOSICION = 1200


class ExpedienteForm(forms.ModelForm):

    letra = forms.ChoiceField(required=False, choices=LETRAS)
    numero = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    anio = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha = forms.DateField(required=True)
    empleado_solicitante = forms.ModelChoiceField(
        required=True, queryset=Empleado.objects.all())
    estado = forms.ModelChoiceField(
        widget=forms.Select(), required=True,
        queryset=Estado.objects.all(), initial=1)
    clase = forms.ModelChoiceField(
        required=True, queryset=Clase.objects.all())
    tipo_resolucion = forms.ModelChoiceField(
        required=False, queryset=TipoResolucion.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpedienteForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha no puede ser posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    class Meta:
        model = Expediente
        fields = '__all__'


class ExpedienteResolucionForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(
        required=True, queryset=Etapa.objects.filter(resolucion=1))

    caja_chica = forms.CharField(required=False)
    resolucion_adjudicacion = forms.CharField(required=False)
    fecha_resolucion_adjudicacion = forms.DateField(required=False)
    proveedor = forms.ModelChoiceField(
        required=False, queryset=Proveedor.objects.all())
    importe = forms.CharField(required=True)
    tipo_transaccion = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    numero_identificacion_transaccion = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    orden_provision = forms.IntegerField(required=False)

    acta_recepcion = forms.IntegerField(required=False)

    numero_resolucion_pago = forms.IntegerField(required=False)
    fecha_resolucion_pago = forms.DateField(
        required=True, initial='01/01/1900')
    fuente_financiamiento = forms.ModelChoiceField(
        required=False, queryset=FuenteFinanciamiento.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpedienteResolucionForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion_adjudicacion'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            if (name == 'importe' or name == 'tipo_transaccion' or
                    name == 'numero_identificacion_transaccion'):
                continue
            field.widget.attrs.update({'class': 'form-control'})

    def clean_resolucion_adjudicacion(self):
        resolucion_adjudicacion = self.cleaned_data['resolucion_adjudicacion']

        if resolucion_adjudicacion:
            if not helpers.numero_es_valido(
                'RESOLUCION_PAGO', resolucion_adjudicacion):
                raise forms.ValidationError(
                    "RESOLUCIÓN DE ADJUDICACIÓN no válido")

        return resolucion_adjudicacion

    def clean_fecha_resolucion_adjudicacion(self):
        fecha = self.cleaned_data['fecha_resolucion_adjudicacion']

        if not fecha:
            return fecha

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de adjudicacion no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise forms.ValidationError("Fecha no válida")

        return fecha

    def clean_fecha_resolucion_pago(self):
        fecha = self.cleaned_data['fecha_resolucion_pago']

        if not fecha:
            return fecha

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de pago no puede ser posterior '
                    'a la actual')
        except ValueError:
            raise forms.ValidationError("Fecha no válida")

        return fecha

    def clean_orden_provision(self):
        orden_provision = self.cleaned_data['orden_provision']

        if orden_provision:
            if not helpers.numero_es_valido('ORDEN_PROVISION', orden_provision):
                raise forms.ValidationError("ORDEN PROVISION no válido")

        return orden_provision

    def clean_acta_recepcion(self):
        acta_recepcion = self.cleaned_data['acta_recepcion']

        if acta_recepcion:
            if not helpers.numero_es_valido('ACTA_RECEPCION', acta_recepcion):
                raise forms.ValidationError("ACTA RECEPCION no válido")

        return acta_recepcion

    def clean_numero_resolucion_pago(self):
        nro_resolucion_pago = self.cleaned_data['numero_resolucion_pago']

        if nro_resolucion_pago:
            if not helpers.numero_es_valido(
                    'RESOLUCION_PAGO', nro_resolucion_pago):
                raise forms.ValidationError("NRO RESOLUCION PAGO no válido")

        return nro_resolucion_pago

    class Meta:
        model = ExpedienteResolucion
        fields = '__all__'
        exclude = []


class ExpedienteDisposicionForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(required=True,
                                   queryset=Etapa.objects.filter(disposicion=1))

    contratacion_directa = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    proveedor = forms.ModelChoiceField(
        required=True, queryset=Proveedor.objects.all())
    importe = forms.FloatField(required=True)

    numero_disposicion = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    fuente_financiamiento = forms.ModelChoiceField(
        required=True, queryset=FuenteFinanciamiento.objects.all())

    fecha_disposicion = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        super(ExpedienteDisposicionForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_disposicion'].initial = fecha

        self.fields['contratacion_directa'].initial = \
            helpers.get_numero_autoincremental('CONTRATACION_DIRECTA')

        self.fields['numero_disposicion'].initial = \
            helpers.get_numero_autoincremental('NUMERO_DISPOSICION')

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({
                'class': 'form-control'})

    def clean_fecha_disposicion(self):
        fecha = self.cleaned_data['fecha_disposicion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de disposicion no puede ser posterior a la '
                    'actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    def clean_importe(self):
        data = self.cleaned_data['importe']

        if type(data) != float:
            raise forms.ValidationError("Ingrese solo números por favor")

        if float(data) >= float(IMPORTE_MAXIMO_TRANSACCION_DISPOSICION):
            raise forms.ValidationError(
                "Verifique el importe ingresado, debe ser menor a $1200")

        return data

    class Meta:
        model = ExpedienteDisposicion
        fields = '__all__'
        exclude = []


class ExpedienteServicioMedicoForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(required=True,
        queryset=Etapa.objects.filter(servicio_medico=1))
    servicio_administracion = forms.ModelChoiceField(required=False,
        queryset=ServicioAdministracion.objects.all())
    profesional = forms.ModelChoiceField(required=False,
        queryset=Empleado.objects.all())
    resolucion_contratacion = forms.CharField(required=True)
    numero_contratacion = forms.CharField(required=True)
    fecha_resolucion_contratacion = forms.DateField(required=True)
    orden_provision = forms.IntegerField(required=False)
    acta_recepcion = forms.IntegerField(required=False)
    numero_resolucion_pago = forms.IntegerField(required=False)
    fecha_resolucion_pago = forms.DateField(required=True)
    importe = forms.CharField(required=True)
    tipo_transaccion = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    numero_identificacion_transaccion = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    solicitante_resolucion_pago = forms.ModelChoiceField(required=True,
        queryset=Empleado.objects.all())
    fuente_financiamiento = forms.ModelChoiceField(
        required=True, queryset=FuenteFinanciamiento.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpedienteServicioMedicoForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion_contratacion'].initial = fecha
        self.fields['fecha_resolucion_pago'].initial = fecha

        numero = helpers.get_numero_autoincremental('NUMERO_CONTRATACION')
        self.fields['numero_contratacion'].initial = numero

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            if (name == 'importe' or name == 'tipo_transaccion' or
                    name == 'numero_identificacion_transaccion'):
                continue
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_resolucion_contratacion(self):
        fecha = self.cleaned_data['fecha_resolucion_contratacion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de contratacion no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    def clean_fecha_resolucion_pago(self):
        fecha = self.cleaned_data['fecha_resolucion_pago']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de pago no puede ser posterior a '
                    'la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    def clean_orden_provision(self):
        orden_provision = self.cleaned_data['orden_provision']

        if orden_provision:
            if not helpers.numero_es_valido('ORDEN_PROVISION', orden_provision):
                raise forms.ValidationError("ORDEN PROVISION no válido")

        return orden_provision

    def clean_acta_recepcion(self):
        acta_recepcion = self.cleaned_data['acta_recepcion']

        if acta_recepcion:
            if not helpers.numero_es_valido('ACTA_RECEPCION', acta_recepcion):
                raise forms.ValidationError("ACTA RECEPCION no válido")

        return acta_recepcion

    def clean_numero_resolucion_pago(self):
        nro_resolucion_pago = self.cleaned_data['numero_resolucion_pago']

        if nro_resolucion_pago:
            if not helpers.numero_es_valido(
                    'RESOLUCION_PAGO', nro_resolucion_pago):
                raise forms.ValidationError("NRO RESOLUCION PAGO no válido")

        return nro_resolucion_pago

    class Meta:
        model = ExpedienteServicioMedico
        fields = '__all__'
        exclude = []


class ExpedienteComodatoForm(forms.ModelForm):

    proveedor = forms.ModelChoiceField(required=True,
      queryset=Proveedor.objects.all())
    resolucion_contratacion = forms.CharField(required=True)
    fecha_resolucion_contratacion = forms.DateField(required=True)
    numero_contratacion_directa = forms.CharField(required=True)
    importe = forms.CharField(required=True)
    orden_provision = forms.CharField(required=True)
    resolucion_pago = forms.CharField(required=True)
    fecha_resolucion_pago = forms.DateField(required=True)
    solicitante_resolucion_pago = forms.ModelChoiceField(required=True,
        queryset=Empleado.objects.all())
    fuente_financiamiento = forms.ModelChoiceField(
        required=True, queryset=FuenteFinanciamiento.objects.all())
    observaciones = forms.CharField(required=False)
    etapa = forms.ModelChoiceField(
        required=True, queryset=Etapa.objects.filter(comodato=1))

    def __init__(self, *args, **kwargs):
        super(ExpedienteComodatoForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion_contratacion'].initial = fecha
        self.fields['fecha_resolucion_pago'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_resolucion_contratacion(self):
        fecha = self.cleaned_data['fecha_resolucion_contratacion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de contratacion no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    def clean_fecha_resolucion_pago(self):
        fecha = self.cleaned_data['fecha_resolucion_pago']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de pago no puede ser posterior a '
                    'la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    class Meta:
        model = ExpedienteComodato
        fields = '__all__'
        exclude = []


class ExpedienteLicitacionForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(
        required=True, queryset=Etapa.objects.filter(licitacion=1))
    numero = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    anio = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    numero_disposicion = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    resolucion_aprobacion = forms.CharField(required=True)
    fecha_resolucion_aprobacion = forms.DateField(required=True)
    resolucion_adjudicacion = forms.CharField(required=False)
    fecha_resolucion_adjudicacion = forms.DateField(required=True)
    fuente_financiamiento = forms.ModelChoiceField(
        required=True, queryset=FuenteFinanciamiento.objects.all())

    proveedor = forms.ModelChoiceField(
        required=False, queryset=Proveedor.objects.all())
    monto = forms.FloatField(required=False)
    monto_total = forms.FloatField(required=False)
    orden_provision = forms.CharField(required=False)
    numero_resolucion_pago = forms.CharField(required=False)
    fecha_resolucion_pago = forms.DateField(required=False)
    solicitante_resolucion_pago = forms.ModelChoiceField(
        required=False, queryset=Empleado.objects.all())
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(ExpedienteLicitacionForm, self).__init__(*args, **kwargs)

        fecha = datetime.now()
        anio = str(fecha.year)[2:]

        self.fields['numero'].initial = \
            helpers.get_numero_autoincremental('NUMERO_LICITACION')

        self.fields['anio'].initial = anio

        self.fields['numero_disposicion'].initial = \
            helpers.get_numero_autoincremental('NUMERO_DISPOSICION')

        self.fields['fecha_resolucion_aprobacion'].initial = fecha

        self.fields['fecha_resolucion_adjudicacion'].initial = fecha

        self.fields['fecha_resolucion_pago'].initial = fecha

        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_resolucion_aprobacion(self):
        fecha = self.cleaned_data['fecha_resolucion_aprobacion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de aprobación no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    def clean_fecha_resolucion_adjudicacion(self):
        fecha = self.cleaned_data['fecha_resolucion_adjudicacion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de adjudicación no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    class Meta:
        model = ExpedienteLicitacion
        fields = '__all__'
        exclude = []


class ExpedienteResolucionesVariasForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(required=True,
        queryset=Etapa.objects.filter(resoluciones_varias=1))
    resolucion_pago = forms.IntegerField(required=False)
    fecha_resolucion_pago = forms.DateField(required=False)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(ExpedienteResolucionesVariasForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion_pago'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_resolucion_pago(self):
        resolucion_pago = self.cleaned_data['resolucion_pago']

        if resolucion_pago:
            if not helpers.numero_es_valido(
                    'RESOLUCION_PAGO', resolucion_pago):
                raise forms.ValidationError("NRO RESOLUCION PAGO no válido")

        return resolucion_pago

    def clean_fecha_resolucion_pago(self):
        fecha = self.cleaned_data['fecha_resolucion_pago']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de pago no puede ser posterior '
                    'a la actual')
        except ValueError:
            raise forms.ValidationError("Fecha no válida")

        return fecha

    class Meta:
        model = ExpedienteResolucionesVarias
        fields = '__all__'
        exclude = []


class ExpedienteResolucionContratacionForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(
        required=True, queryset=Etapa.objects.filter(resolucion_contratacion=1))
    proveedor = forms.ModelChoiceField(
        required=True, queryset=Proveedor.objects.all())
    numero_resolucion = forms.IntegerField(required=False)
    fecha_resolucion = forms.DateField(required=True)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(ExpedienteResolucionContratacionForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({
                'class': 'form-control'})

    def clean_numero_resolucion(self):
        numero = self.cleaned_data['numero_resolucion']

        if numero:
            if not helpers.numero_es_valido('RESOLUCION_PAGO', numero):
                raise forms.ValidationError("NRO RESOLUCION no válido")

        return numero

    def clean_fecha_resolucion(self):
        fecha = self.cleaned_data['fecha_resolucion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion no puede ser posterior a la '
                    'actual')
        except ValueError:
            raise ValueError("Fecha no válida")

        return fecha

    class Meta:
        model = ExpedienteResolucionContratacion
        fields = '__all__'
        exclude = []