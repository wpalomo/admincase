# -*- coding: utf-8 -*-

from django import forms

from apps.complementos.salud.models import UnidadMedida

from .models import Catalogo

from . import helpers
from .models import (Medicamento, PrincipioActivo, LineaTerapeutica,
                     ViaAdministracion, FormaFarmaceutica,
                     MedicamentoLaboratorio, Laboratorio, Envase, Agrupado,
                     Pack, Pallet)


class MedicamentoForm(forms.ModelForm):

    catalogo = forms.ModelChoiceField(
        required=True, queryset=Catalogo.objects.all())
    codigo = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    denominacion = forms.CharField(required=True)

    producto_combinado = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'flat'}))
    libre_azucar = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'flat'}))
    libre_conservante = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'flat'}))
    libre_cfc = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'flat'}))
    libre_gluten = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'flat'}))

    principio_activo = forms.ModelChoiceField(
        required=False, queryset=PrincipioActivo.objects.all())
    potencia_numerador = forms.IntegerField(required=False)
    unidad_medida_numerador = forms.ModelChoiceField(
        required=False, queryset=UnidadMedida.objects.all())
    potencia_denominador = forms.IntegerField(required=False)
    unidad_medida_denominador = forms.ModelChoiceField(
        required=False, queryset=UnidadMedida.objects.all())
    linea_terapeutica = forms.ModelChoiceField(
        required=False, queryset=LineaTerapeutica.objects.all())
    via_administracion = forms.ModelChoiceField(
        required=False, queryset=ViaAdministracion.objects.all())
    forma_farmaceutica = forms.ModelChoiceField(
        required=False, queryset=FormaFarmaceutica.objects.all())

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)

        self.set_initial_values()
        self.set_css_controls()

    def set_initial_values(self):
        self.fields['codigo'].initial = \
            helpers.get_numero_autoincremental('MEDICAMENTO')

    def set_css_controls(self):

        for name, field in list(self.fields.items()):
            self.fields['producto_combinado'].widget.attrs['class'] = 'flat'
            self.fields['libre_azucar'].widget.attrs['class'] = 'flat'
            self.fields['libre_conservante'].widget.attrs['class'] = 'flat'
            self.fields['libre_cfc'].widget.attrs['class'] = 'flat'
            self.fields['libre_gluten'].widget.attrs['class'] = 'flat'

            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Medicamento
        fields = '__all__'


class MedicamentoLaboratorioForm(forms.ModelForm):

    medicamento = forms.ModelChoiceField(
        required=True, queryset=Medicamento.objects.all())
    nombre_comercial = forms.CharField(required=True, max_length=100)
    laboratorio = forms.ModelChoiceField(required=True,
                                         queryset=Laboratorio.objects.all())
    numero_certificado = forms.IntegerField(required=False)
    numero_gtin = forms.CharField(required=False, max_length=14, min_length=12,
                                  widget=forms.NumberInput(
                                      attrs=({'class': 'form-control'})))
    forma_farmaceutica = forms.ModelChoiceField(
        required=True, queryset=FormaFarmaceutica.objects.all())
    envase_primario = forms.ModelChoiceField(required=True,
                                             queryset=Envase.objects.all())
    cantidad_envase_primario = forms.IntegerField(required=False)
    unidad_medida_envase_primario = forms.ModelChoiceField(
        required=False, queryset=UnidadMedida.objects.all())
    envase_secundario = forms.ModelChoiceField(
        required=False, queryset=Envase.objects.all())
    cantidad_envase_secundario = forms.IntegerField(required=False)
    unidad_medida_envase_secundario = forms.ModelChoiceField(
        required=False, queryset=UnidadMedida.objects.all())
    agrupado_cantidad = forms.IntegerField(required=False)
    agrupado_unidad = forms.ModelChoiceField(required=False,
                                             queryset=Agrupado.objects.all())
    pack_cantidad = forms.IntegerField(required=True)
    pack_unidad_despacho = forms.ModelChoiceField(required=True,
                                                  queryset=Pack.objects.all())
    pallet_cantidad = forms.IntegerField(required=False)
    pallet_unidad_logistica = forms.ModelChoiceField(required=False,
                                                     queryset=
                                                     Pallet.objects.all())

    def __init__(self, *args, **kwargs):

        super(MedicamentoLaboratorioForm, self).__init__(*args, **kwargs)
        self.set_css_controls()

    def set_css_controls(self):

        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:

        model = MedicamentoLaboratorio
        fields = '__all__'
