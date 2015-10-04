# -*- coding: utf-8 -*-

from datetime import datetime
from django import forms
from apps.complementos.persona.models import TipoDocumento, Sexo
from apps.personas.models import Persona
from .models import Cliente


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            print(name)
            field.widget.attrs.update({
                'class': 'form-control has-feedback-right'
            })

    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['persona']


class PersonaForm(forms.ModelForm):
    apellido = forms.CharField(required=True)
    nombre = forms.CharField(required=True)
    tipo_documento = forms.ModelChoiceField(
        required=True, queryset=TipoDocumento.objects.all())
    numero_documento = forms.CharField(required=True)
    sexo = forms.ModelChoiceField(
        required=True, queryset=Sexo.objects.all())

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