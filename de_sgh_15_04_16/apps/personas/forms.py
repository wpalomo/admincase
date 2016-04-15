# -*- coding: utf-8 -*-
from django import forms

from django.forms.utils import ErrorList

from .models import PersonaObraSocial
from apps.complementos.obrasocial.models import ObraSocial, MotivoSuspension
from apps.complementos.paciente.models import Categoria
from apps.complementos.persona.models import Parentesco


class PersonaObraSocialForm(forms.ModelForm):

    obra_social = forms.ModelChoiceField(
        queryset=ObraSocial.objects.all(), required=True)

    parentesco = forms.ModelChoiceField(
        queryset=Parentesco.objects.all(), required=False)

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(), required=True)

    motivo_suspension = forms.ModelChoiceField(
        queryset=MotivoSuspension.objects.all(), required=False)

    suspendida = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(PersonaObraSocialForm, self).__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        if self.cleaned_data['motivo_suspension'] is None:
            if 'suspendida' in self.cleaned_data:
                if self.cleaned_data['suspendida'] is True:
                    errors = self._errors.setdefault("motivo_suspension",
                        ErrorList())
                    errors.append('Ingrese el motivo de suspensión')

        return super(PersonaObraSocialForm, self).clean()

    class Meta:
        model = PersonaObraSocial
        fields = '__all__'
        exclude = ['persona']
