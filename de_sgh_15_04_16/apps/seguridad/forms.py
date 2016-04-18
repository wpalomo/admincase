# -*- coding: utf-8 -*-

from django import forms

from apps.complementos.arbolitem.models import ArbolItem
from apps.instituciones.models import Institucion

from .models import Perfil, PerfilModulo


class PerfilForm(forms.ModelForm):

    institucion = forms.ModelChoiceField(
        required=True, queryset=Institucion.objects.all())
    nombre = forms.CharField(required=True)
    descripcion = forms.CharField(required=False)

    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ['valor']


class PerfilModuloForm(forms.ModelForm):

    perfil = forms.ModelChoiceField(
        required=True, queryset=Perfil.objects.all())
    modulo = forms.ModelChoiceField(
        required=True, queryset=ArbolItem.objects.filter(padre_id=0))

    class Meta:
        model = PerfilModulo
        fields = '__all__'
        exclude = ['']
