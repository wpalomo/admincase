# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms

from apps.empleados.models import Empleado
from apps.proveedores.models import Proveedor

from . import helpers
from .models import (Expediente, ExpedienteResolucion, ExpedienteDisposicion,
                     ExpedienteServicioMedico, ExpedienteLicitacion, Estado,
                     Etapa, Clase, FuenteFinanciamiento, ExpedienteComodato)


LETRAS = (('A', 'A'), ('C', 'C'), ('G', 'G'),
          ('H', 'H'), ('P', 'P'), ('S', 'S'),)

IMPORTE_MAXIMO_TRANSACCION_DISPOSICION = 1200


class ExpedienteForm(forms.ModelForm):

    letra = forms.ChoiceField(required=True, choices=LETRAS)
    numero = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    anio = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha = forms.DateField(required=True)
    empleado_solicitante = forms.ModelChoiceField(
        required=True, queryset=Empleado.objects.all())
    estado = forms.ModelChoiceField(
        widget=forms.Select(), required=True,
        queryset=Estado.objects.all(), initial=1)
    clase = forms.ModelChoiceField(
        required=True, queryset=Clase.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpedienteForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha'].initial = fecha

        self.fields['numero'].initial = self.generar_numero_expediente()

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            # if name == 'letra' or name == 'numero' or name == 'anio':
            #     continue
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha no puede ser posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha

    def generar_numero_expediente(self):

        try:
            expediente = Expediente.objects.latest('id')
            numero = int(expediente.numero) + 1
        except:
            numero = 1

        return numero

    class Meta:
        model = Expediente
        fields = '__all__'


class ExpedienteResolucionForm(forms.ModelForm):

    etapa = forms.ModelChoiceField(
        required=True, queryset=Etapa.objects.filter(resolucion=1))

    resolucion_adjudicacion = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    fecha_resolucion_adjudicacion = forms.DateField(required=True)
    proveedor = forms.ModelChoiceField(
        required=True, queryset=Proveedor.objects.all())
    importe = forms.CharField(required=True)
    tipo_transaccion = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    numero_identificacion_transaccion = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    orden_provision = forms.CharField(required=True, initial=0)
    acta_recepcion = forms.CharField(required=True, initial=0)
    numero_resolucion_pago = forms.CharField(required=True, initial=0)
    fecha_resolucion_pago = forms.DateField(
        required=True, initial='01/01/1900')
    fuente_financiamiento = forms.ModelChoiceField(
        required=True, queryset=FuenteFinanciamiento.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExpedienteResolucionForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_resolucion_adjudicacion'].initial = fecha

        self.fields['resolucion_adjudicacion'].initial = \
            helpers.get_numero_autoincremental('RESOLUCION_ADJUDICACION')
        self.fields['orden_provision'].initial = \
            helpers.get_numero_autoincremental('ORDEN_PROVISION')
        self.fields['acta_recepcion'].initial = \
            helpers.get_numero_autoincremental('ACTA_RECEPCION')

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            if (name == 'importe' or name == 'tipo_transaccion' or
                    name == 'numero_identificacion_transaccion'):
                continue
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_resolucion_adjudicacion(self):
        fecha = self.cleaned_data['fecha_resolucion_adjudicacion']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de adjudicacion no puede ser '
                    'posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha

    def clean_fecha_resolucion_pago(self):
        fecha = self.cleaned_data['fecha_resolucion_pago']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError(
                    'La fecha de resolucion de pago no puede ser posterior '
                    'a la actual')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha

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
            raise ValueError("Fecha no valida")

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

    profesional = forms.ModelChoiceField(required=True,
        queryset=Empleado.objects.all())
    resolucion_contratacion = forms.CharField(required=True)
    fecha_resolucion_contratacion = forms.DateField(required=True)
    orden_provision = forms.CharField(required=True, initial=0)
    acta_recepcion = forms.CharField(required=True, initial=0)
    numero_resolucion_pago = forms.CharField(required=True, initial=0)
    fecha_resolucion_pago = forms.DateField(required=True)
    importe = forms.CharField(required=True)
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
            raise ValueError("Fecha no valida")

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
            raise ValueError("Fecha no valida")

        return fecha

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
    etapa = forms.ModelChoiceField(required=True, queryset=Etapa.objects.filter(comodato=1))


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
            raise ValueError("Fecha no valida")

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
            raise ValueError("Fecha no valida")

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
    resolucion_adjudicacion = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
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

        self.fields['resolucion_adjudicacion'].initial = \
            helpers.get_numero_autoincremental('RESOLUCION_ADJUDICACION')

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
            raise ValueError("Fecha no valida")

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
            raise ValueError("Fecha no valida")

        return fecha

    class Meta:
        model = ExpedienteLicitacion
        fields = '__all__'
        exclude = []
