# -*- coding: utf-8 -*-

from django import forms

from apps.personas.models import Persona
from .models import Tramite, RequisitoPresentado


class TramiteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TramiteForm, self).__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            if name == 'estado':
                continue
            field.widget.attrs.update({'class': 'form-control'})

    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all()
    )

    class Meta:
        model = Tramite
        fields = '__all__'
        exclude = []