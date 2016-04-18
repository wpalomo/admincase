# -*- coding: utf-8 -*-

from datetime import datetime
from django import forms
from django.forms.utils import ErrorList

from apps.complementos.organigrama.models import (Cargo, Direccion,
                                                  Departamento, Division,
                                                  Servicio, Seccion)
from apps.complementos.persona.models import TipoDocumento, Sexo
from apps.instituciones.models import Institucion
from apps.personas.models import Persona

from . import helpers
from .models import Empleado, AsignacionFormal


class EmpleadoForm(forms.ModelForm):

    instancia = ''

    fecha_ingreso = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.instancia = kwargs['instance']

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_ingreso(self):
        fecha = self.cleaned_data['fecha_ingreso']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
            if fecha > datetime.now().date():
                raise forms.ValidationError('La fecha de ingreso no puede '
                                            'ser posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha

    class Meta:
        model = Empleado
        fields = '__all__'
        exclude = ['persona']


class PersonaForm(forms.ModelForm):

    '''
    instancia: este atributo se utiliza en la función
    clean_numero_documento. Verifica
    si es actualizar o crear.
    '''

    instancia = ''

    tipo_documento = forms.ModelChoiceField(
        required=True, queryset=TipoDocumento.objects.all())
    sexo = forms.ModelChoiceField(required=True, queryset=Sexo.objects.all())
    fecha_nacimiento = forms.DateField(initial='1900-01-01')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.instancia = kwargs['instance']
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']

        if str.isnumeric(apellido):
            raise forms.ValidationError("Ingrese apellido texto")

        return apellido.upper()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if str.isnumeric(nombre):
            raise forms.ValidationError("Ingrese nombre texto")

        return nombre.upper()

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']

        try:
            datetime.strptime(str(fecha_nacimiento), '%Y-%m-%d')
            if fecha_nacimiento > datetime.now().date():
                raise forms.ValidationError('La fecha de nacimiento no puede '
                                            'ser posterior a la actual')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_nacimiento

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data['numero_documento']
        if self.instancia == '':
            persona = Persona.objects.filter(numero_documento=numero_documento)
            if len(persona) > 0:
                empleado = Empleado.objects.filter(persona=persona)
                if len(empleado) > 0:
                    raise forms.ValidationError('El empleado ya se '
                                                'encuentra registrado en '
                                                'el sistema de salud')
        return numero_documento

    def clean(self):
        if 'tipo_documento' in self.cleaned_data:
            if 'numero_documento' in self.cleaned_data:
                tipo_documento = self.cleaned_data['tipo_documento']
                numero_documento = self.cleaned_data['numero_documento']
                tipos_documentos = TipoDocumento.objects.filter(abreviatura=
                                                                tipo_documento)\
                    .values('longitud')
                for tipo in tipos_documentos:
                    if len(numero_documento) > tipo['longitud']:
                        errors = self._errors.setdefault("numero_documento",
                                                         ErrorList())
                        errors.append('La longitud del '
                                      'Tipo de Documento'
                                      ' no corresponde')
        return super(PersonaForm, self).clean()

    class Meta:
        model = Persona
        fields = '__all__'


class AsignacionFormalForm(forms.ModelForm):

    destino = forms.ModelChoiceField(
        required=True, queryset=Institucion.objects.all())
    cargo = forms.ModelChoiceField(
        required=False, queryset=Cargo.objects.all())
    direccion = forms.ModelChoiceField(
        required=False, queryset=Direccion.objects.all())
    departamento = forms.ModelChoiceField(
        required=False, queryset=Departamento.objects.all())
    division = forms.ModelChoiceField(
        required=False, queryset=Division.objects.all())
    servicio = forms.ModelChoiceField(
        required=False, queryset=Servicio.objects.all())
    seccion = forms.ModelChoiceField(
        required=False, queryset=Seccion.objects.all())
    fecha_desde = forms.DateField(required=True)
    fecha_hasta = forms.DateField(required=True)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(AsignacionFormalForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_desde'].initial = fecha
        self.fields['fecha_hasta'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({
                'class': 'form-control'})

    def clean_fecha_desde(self):
        fecha_desde = self.cleaned_data['fecha_desde']

        try:
            datetime.strptime(str(fecha_desde), '%Y-%m-%d')

            if 'fecha_hasta' in self.cleaned_data:

                fecha_hasta = self.cleaned_data['fecha_hasta']

                if fecha_desde >= fecha_hasta:
                    raise forms.ValidationError('La fecha desde no puede '
                                                'ser mayor a la fecha desde '
                                                'cargada')

        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_desde

    def clean_fecha_hasta(self):

        fecha_hasta = self.cleaned_data['fecha_hasta']

        try:
            datetime.strptime(str(fecha_hasta), '%Y-%m-%d')

            if 'fecha_desde' in self.cleaned_data:

                fecha_desde = self.cleaned_data['fecha_desde']

                if fecha_hasta <= fecha_desde:
                    raise forms.ValidationError('La fecha hasta no puede '
                                                'ser menor ni igual a la '
                                                'fecha desde cargada')

        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_hasta

    class Meta:
        model = AsignacionFormal
        fields = '__all__'