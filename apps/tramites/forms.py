# -*- coding: utf-8 -*-

from django import forms

from .models import Tramite


class TramiteForm(forms.ModelForm):

    class Meta:
        model = Tramite
        fields = '__all__'
        exclude = []
