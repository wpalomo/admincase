# -*- coding: utf-8 -*-

from django import forms

from apps.complementos.organigrama.models import Entidad
# from apps.personas.models import Persona
from .models import Tramite, TipoTramite, Requisito


# class TipoTramiteForm(forms.ModelForm):
#
#     descripcion = forms.CharField(required=True)
#     entidad = forms.ModelChoiceField(
#         queryset=Entidad.objects.all(), required=True)
#
#     requisitos = forms.ModelMultipleChoiceField(
#         queryset=Requisito.objects.all(), required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(TramiteForm, self).__init__(*args, **kwargs)
#         for name, field in list(self.fields.items()):
#             if name == 'estado':
#                 continue
#             field.widget.attrs.update({'class': 'form-control'})
#
#     class Meta:
#         model = Tramite
#         fields = '__all__'
#         exclude = []

class TramiteForm(forms.ModelForm):

    # persona = forms.ModelChoiceField(
    #     queryset=Persona.objects.all(), required=True)

    tipo = forms.ModelChoiceField(
        queryset=TipoTramite.objects.all(), required=True)
    fecha_inicio = forms.DateTimeField(required=True)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(TramiteForm, self).__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            if name == 'estado':
                continue
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tramite
        fields = '__all__'
        exclude = []