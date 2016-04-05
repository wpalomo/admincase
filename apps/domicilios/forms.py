# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import ErrorList

from apps.complementos.locacion.models import Pais, Provincia

from .models import Domicilio


class DomicilioForm(forms.ModelForm):

    pais = forms.ModelChoiceField(queryset=Pais.objects.all(),
                                  required=True)
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(),
                                       required=True)

    def __init__(self, *args, **kwargs):
        super(DomicilioForm, self).__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):

        return super(DomicilioForm, self).clean()

    class Meta:
        model = Domicilio
        fields = '__all__'
        exclude = ['persona']
