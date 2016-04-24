# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms

from apps.complementos.persona.models import (TipoDocumento, Sexo, EstadoCivil,
                                              NivelEducacion)
from apps.complementos.salud.models import ObraSocial
from apps.complementos.organigrama.models import Profesion
from apps.clientes.models import Cliente
from .models import Persona


class PersonaForm(forms.ModelForm):

    '''
    instancia: este atributo se utiliza en la función
    clean_numero_documento. Verifica
    si es actualizar o crear.
    '''

    instancia = ''

    foto = forms.ImageField(required=False)
    apellido = forms.CharField(required=True)
    nombre = forms.CharField(required=True)
    tipo_documento = forms.ModelChoiceField(
        required=True, queryset=TipoDocumento.objects.all())
    numero_documento = forms.CharField(required=True)
    sexo = forms.ModelChoiceField(
        required=True, queryset=Sexo.objects.all())
    fecha_nacimiento = forms.DateField(required=False)
    estado_civil = forms.ModelChoiceField(
        required=False, queryset=EstadoCivil.objects.all())
    obra_social = forms.ModelChoiceField(
        required=False, queryset=ObraSocial.objects.all())
    nivel_educacion = forms.ModelChoiceField(
        required=False, queryset=NivelEducacion.objects.all())
    profesion = forms.ModelChoiceField(
        required=False, queryset=Profesion.objects.all())
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.instancia = kwargs['instance']
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control has-feedback-right'
            })

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']

        if str.isnumeric(apellido):
            raise forms.ValidationError("Ingrese apellido texto")

        return apellido

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if str.isnumeric(nombre):
            raise forms.ValidationError("Ingrese nombre texto")

        return nombre

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']

        if fecha_nacimiento:

            try:
                datetime.strptime(str(fecha_nacimiento), '%Y-%m-%d')
                if fecha_nacimiento > datetime.now().date():
                    raise forms.ValidationError('La fecha de nacimiento no puede '
                                                'ser mayor a la actual')
            except ValueError:
                raise ValueError("Fecha no valida")

        return fecha_nacimiento

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data['numero_documento']
        if self.instancia == '':
            persona = Persona.objects.filter(numero_documento=numero_documento)
            if len(persona) > 0:
                cliente = Cliente.objects.filter(persona=persona)
                if len(cliente) > 0:
                    raise forms.ValidationError('El cliente ya se '
                                                'encuentra registrado en '
                                                'el sistema!')
        return numero_documento

    class Meta:
        model = Persona
        fields = '__all__'
