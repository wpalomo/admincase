# -*- coding: utf-8 -*-

from django import forms

from .models import Cliente
from apps.clientes.models import SituacionLaboral


class ClienteForm(forms.ModelForm):

    cuil = forms.CharField(required=False)
    fecha_alta = forms.DateField(required=False)
    situacion_laboral = forms.ModelChoiceField(
        required=False, queryset=SituacionLaboral.objects.all())

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name)
            field.widget.attrs.update({
                'class': 'form-control has-feedback-right'
            })

    class Meta:
        model = Cliente
        fields = '__all__'