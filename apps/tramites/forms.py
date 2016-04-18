# -*- coding: utf-8 -*-
from datetime import datetime
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

    tipo = forms.ModelChoiceField(
        queryset=TipoTramite.objects.all(), required=True)
    fecha_alta = forms.DateTimeField(required=False)
    fecha_turno = forms.DateField(required=False)
    fecha_alarma = forms.DateField(required=False)
    # estado = forms.BooleanField(initial=1)
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super(TramiteForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_alta'].initial = fecha

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            if name == 'estado':
                continue
            # if name == 'tipo':
            #     field.widget.attrs.update({'class': 'form-control select2_single'})
            #     continue

            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_turno(self):
        fecha = self.cleaned_data['fecha_turno']

        if fecha:
            try:
                datetime.strptime(str(fecha), '%Y-%m-%d')

                if fecha < datetime.now().date():
                    raise forms.ValidationError('La fecha del turno no puede '
                                                'ser menor a la actual')
            except ValueError:
                raise ValueError("Fecha no valida")

        return fecha

    def clean_fecha_alarma(self):
        fecha = self.cleaned_data['fecha_alarma']

        if fecha:
            try:
                datetime.strptime(str(fecha), '%Y-%m-%d')

                if fecha <= datetime.now().date():
                    raise forms.ValidationError('La fecha de alarma no puede '
                                                'ser menor o igual a la actual')
            except ValueError:
                raise ValueError("Fecha no valida")

        return fecha

    class Meta:
        model = Tramite
        fields = '__all__'