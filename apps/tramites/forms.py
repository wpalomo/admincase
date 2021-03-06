# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from apps.complementos.organigrama.models import Entidad
# from apps.personas.models import Persona
from .models import Tramite, TipoTramite, Requisito


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
        self.fields['fecha_alta'].initial = datetime.now()

    def set_css_controls(self):
        for name, field in list(self.fields.items()):

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


class TipoTramiteForm(forms.ModelForm):

    descripcion = forms.CharField(max_length=50, required=True)
    entidad = forms.ModelChoiceField(
        queryset=Entidad.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(TipoTramiteForm, self).__init__(*args, **kwargs)
        self.set_css_controls()

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})
    #
    # def clean_fecha_turno(self):
    #     fecha = self.cleaned_data['fecha_turno']
    #
    #     if fecha:
    #         try:
    #             datetime.strptime(str(fecha), '%Y-%m-%d')
    #
    #             if fecha < datetime.now().date():
    #                 raise forms.ValidationError('La fecha del turno no puede '
    #                                             'ser menor a la actual')
    #         except ValueError:
    #             raise ValueError("Fecha no valida")
    #
    #     return fecha
    #
    # def clean_fecha_alarma(self):
    #     fecha = self.cleaned_data['fecha_alarma']
    #
    #     if fecha:
    #         try:
    #             datetime.strptime(str(fecha), '%Y-%m-%d')
    #
    #             if fecha <= datetime.now().date():
    #                 raise forms.ValidationError('La fecha de alarma no puede '
    #                                             'ser menor o igual a la actual')
    #         except ValueError:
    #             raise ValueError("Fecha no valida")
    #
    #     return fecha

    class Meta:
        model = TipoTramite
        fields = '__all__'