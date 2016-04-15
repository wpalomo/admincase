from django import forms

from apps.personas.models import Persona
from apps.complementos.persona.models import (TipoDocumento, Sexo, Parentesco)
from apps.complementos.locacion.models import (LugarNacimiento, Pais, Provincia,
                                               Departamento)

from .models import (Familiar, Ocupacion, FamiliarPaciente,
                     SituacionLaboral, TipoRelacion)


class FamiliarForm(forms.ModelForm):

    vive = forms.BooleanField(initial=True, required=False,
                              widget=forms.CheckboxInput())

    motivo_fallecimiento = forms.CharField(required=False,
                                           widget=forms.Textarea())

    ocupacion = forms.ModelChoiceField(required=False,
                                       queryset=Ocupacion.objects.all(),
                                       widget=forms.Select())

    situacion_laboral = forms.ModelChoiceField(required=False,
                                               queryset=
                                               SituacionLaboral.objects.all(),
                                               widget=forms.Select())

    responsable = forms.BooleanField(initial=False, required=False,
                                     widget=forms.CheckboxInput())

    otra_ayuda_economica = forms.CharField(required=False,
                                           widget=forms.TextInput())

    economicamente_activo = forms.BooleanField(initial=False, required=False,
                                               widget=
                                               forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(FamiliarForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Familiar
        fields = '__all__'
        exclude = ['persona']


class PersonaForm(forms.ModelForm):

    tipo_documento = forms.ModelChoiceField(
        required=True, queryset=TipoDocumento.objects.all())
    numero_documento = forms.CharField(required=False,
                                       max_length=200, widget=forms.NumberInput)
    sexo = forms.ModelChoiceField(required=True, queryset=Sexo.objects.all())
    fecha_nacimiento = forms.DateField(initial='01/01/1900')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Persona
        fields = '__all__'


class FamiliarPacienteForm(forms.ModelForm):

    parentesco = forms.ModelChoiceField(required=True,
                                        queryset=Parentesco.objects.all(),
                                        widget=forms.Select())
    
    tipo_relacion = forms.ModelChoiceField(required=False,
                                           queryset=TipoRelacion.objects.all(),
                                           widget=forms.Select())
    
    responsable = forms.BooleanField(initial=False, required=False, widget=
                                     forms.CheckboxInput())

    convive_misma_vivienda = forms.BooleanField(initial=False, required=False,
                                                widget=
                                                forms.CheckboxInput())
    
    observacion = forms.CharField(required=False, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(FamiliarPacienteForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = FamiliarPaciente
        fields = '__all__'
        exclude = ['paciente', 'familiar']


class LugarNacimientoForm(forms.ModelForm):

    pais = forms.ModelChoiceField(required=True, label='País',
                                  queryset=Pais.objects.all(),
                                  widget=forms.Select(
                                      attrs=({'class': 'form-control'})))

    provincia = forms.ModelChoiceField(required=False,
                                       queryset=Provincia.objects.all(),
                                       widget=forms.Select(
                                           attrs=({'class': 'form-control'})))

    departamento = forms.ModelChoiceField(required=False,
                                          queryset=Departamento.objects.all(),
                                          widget=forms.Select(attrs=(
                                              {'class': 'form-control'})))

    class Meta:
        model = LugarNacimiento
        fields = ['pais', 'provincia', 'departamento']
