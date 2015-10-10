# -*- coding: utf-8 -*-

from django import forms

from .models import Domicilio, TipoDomicilio

from apps.complementos.locacion.models import (Pais, Provincia, Departamento,
                                               Localidad)


class DomicilioForm(forms.ModelForm):

    tipo = forms.ModelChoiceField(
        queryset=TipoDomicilio.objects.all(),
        required=False, widget=(forms.Select(attrs=({'class': 'form-control'})))
    )

    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        required=True, widget=(forms.Select(attrs=({'class': 'form-control'})))
    )

    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=True, widget=(forms.Select(attrs=({'class': 'form-control'})))
    )

    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=False, widget=(forms.Select(attrs=({'class': 'form-control'})))
    )

    localidad = forms.ModelChoiceField(
        queryset=Localidad.objects.all(),
        required=False, widget=(forms.Select(attrs=({'class': 'form-control'})))
    )

    descripcion = forms.CharField(
        required=False, widget=(
            forms.TextInput(attrs=({'class': 'form-control'}))
        )
    )

    class Meta:
        model = Domicilio
        fields = '__all__'
        exclude = ['persona']
