# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms

from apps.complementos.persona.models import (TipoDocumento, Sexo, EstadoCivil,
                                              NivelEducacion)
from apps.complementos.salud.models import ObraSocial
from apps.complementos.organigrama.models import Profesion
from .models import Persona


class PersonaForm(forms.ModelForm):

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
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control has-feedback-right'
            })

    def clean_apellido(self):
        data = self.cleaned_data['apellido']

        if str.isnumeric(data):
            raise forms.ValidationError("Ingrese apellido texto")

        return data

    def clean_nombre(self):
        data = self.cleaned_data['nombre']

        if str.isnumeric(data):
            raise forms.ValidationError("Ingrese nombre texto")

        return data

    def clean_fecha_nacimiento(self):
        data = self.cleaned_data['fecha_nacimiento']

        try:
            datetime.strptime(str(data), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha no valida")

        return data

    class Meta:
        model = Persona
        fields = '__all__'
