from django import forms

from apps.personas.models import Persona, Profesion
from apps.pacientes.models import Paciente
from apps.complementos.paciente.models import SituacionLaboral
from apps.complementos.persona.models import EstadoCivil, Etnia, NivelEducacion
from apps.complementos.locacion.models import Pais, Provincia, Departamento, \
    Localidad, Barrio

from .models import FichaSocial, TipoIVA, SituacionPropiedad, TipoVivienda, \
    TerrenoPropio, TipoConstruccion, ServicioAgua, ServicioLuzElectrica,\
    OtroServicio, TipoBanio, TipoPared, TipoPiso, TipoProgramaSocial, TipoTecho


class PersonaForm(forms.ModelForm):

    estado_civil = forms.ModelChoiceField(required=False,
                                          queryset=EstadoCivil.objects.all())
    etnia = forms.ModelChoiceField(required=False,
                                   queryset=Etnia.objects.all(),
                                   widget=forms.Select())

    nivel_educacion = forms.ModelChoiceField(required=False,
                                             queryset=NivelEducacion.objects.all(),
                                             widget=forms.Select())
    profesion = forms.ModelChoiceField(required=False,
                                       queryset=Profesion.objects.all(),
                                       label='Ocupación')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Persona
        fields = ['estado_civil', 'etnia', 'nivel_educacion', 'profesion']


class PacienteForm(forms.ModelForm):

    cuil = forms.CharField(required=False, label="CUIL",
                           widget=forms.TextInput())
    cuit = forms.CharField(required=False, label="CUIT",
                           widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Paciente
        fields = ['cuil', 'cuit']


class FichaSocialForm(forms.ModelForm):

    paciente = forms.ModelChoiceField(Paciente, required=False)

    numero_ficha = forms.CharField(required=True, max_length=None,
                                   widget=forms.TextInput())

    ultima_verificacion = forms.DateField(required=False,
                                          widget=forms.DateInput())

    tipo_iva = forms.ModelChoiceField(required=True,
                                      queryset=TipoIVA.objects.all(),
                                      label='AFIP',
                                      widget=forms.Select())

    situacion_laboral = forms.ModelChoiceField(required=False,
                                               queryset=
                                               SituacionLaboral.objects.all(),
                                               label='Situación Laboral',
                                               widget=forms.Select())

    ingreso_mensual = forms.CharField(required=False,
                                      label='Ingreso Mensual',
                                      widget=forms.TextInput())

    # DATOS DE LA EMPRESA
    lugar_trabajo = forms.CharField(max_length=50, required=False,
                                    label='Lugar de Trabajo',
                                    widget=forms.TextInput())
    pais = forms.ModelChoiceField(required=False, label='País',
                                  queryset=Pais.objects.all(),
                                  widget=forms.Select())
    provincia = forms.ModelChoiceField(required=False,
                                       queryset=Provincia.objects.all(),
                                       widget=forms.Select())
    departamento = forms.ModelChoiceField(required=False,
                                          queryset=Departamento.objects.all(),
                                          widget=forms.Select())
    localidad = forms.ModelChoiceField(required=False,
                                       queryset=Localidad.objects.all(),
                                       widget=forms.Select())
    barrio = forms.ModelChoiceField(required=False,
                                    queryset=Barrio.objects.all(),
                                    widget=forms.Select())
    descripcion_domicilio = forms.CharField(required=False, max_length=3000,
                                            label='Descripción del Domicilio',
                                            widget=forms.Textarea())
    codigo_postal = forms.CharField(required=False, max_length=20,
                                    label='Código Postal',
                                    widget=forms.TextInput())
    # ASPECTOS HABITACIONALES

    situacion_propiedad = forms.ModelChoiceField(required=False,
                                                 queryset=SituacionPropiedad
                                                 .objects.all(),
                                                 widget=forms.Select())
    tipo_vivienda = forms.ModelChoiceField(required=False,
                                           queryset=TipoVivienda.objects.all(),
                                           widget=forms.Select())
    terreno_propio = forms.ModelChoiceField(required=False,
                                            queryset=TerrenoPropio.objects.all(),
                                            widget=forms.Select())
    tipo_construccion = forms.ModelChoiceField(required=False,
                                               queryset=
                                               TipoConstruccion.objects.all(),
                                               widget=forms.Select())
    servicio_agua = forms.ModelChoiceField(required=False,
                                           queryset=ServicioAgua.objects.all(),
                                           widget=forms.Select())

    servicio_luz_electrica = forms.ModelChoiceField(
        required=False,
        queryset=ServicioLuzElectrica.objects.all(),
        widget=forms.Select()
    )

    otro_servicio = forms.ModelChoiceField(required=False,
                                           queryset=OtroServicio.objects.all(),
                                           widget=forms.Select())
    tipo_banio = forms.ModelChoiceField(required=False,
                                        queryset=TipoBanio.objects.all(),
                                        widget=forms.Select())
    tipo_techo = forms.ModelChoiceField(required=False,
                                        queryset=TipoTecho.objects.all(),
                                        widget=forms.Select())
    tipo_pared = forms.ModelChoiceField(required=False,
                                        queryset=TipoPared.objects.all(),
                                        widget=forms.Select())
    tipo_piso = forms.ModelChoiceField(required=False,
                                       queryset=TipoPiso.objects.all(),
                                       widget=forms.Select())

    # CANTIDADES
    cantidad_dormitorio = forms.IntegerField(required=False,
                                             widget=forms.NumberInput())
    cantidad_ambiente = forms.IntegerField(required=False,
                                           widget=forms.NumberInput())
    cantidad_cama = forms.IntegerField(required=False,
                                       widget=forms.NumberInput())
    # PROGRAMAS SOCIALES

    programa_social = forms.ModelMultipleChoiceField(
        required=False, queryset=TipoProgramaSocial.objects.all(),
        widget=forms.SelectMultiple()
    )

    observacion_socio_economica = forms.CharField(
        required=False,
        widget=forms.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(FichaSocialForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = FichaSocial
        fields = '__all__'
