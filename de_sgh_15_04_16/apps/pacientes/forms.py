
from datetime import datetime

from django import forms
from django.forms.utils import ErrorList

from apps.complementos.persona.models import Sexo, TipoDocumento
from apps.personas.models import Persona

from .models import Paciente, TipoPaciente

# siempre variables de clase al principio, antes de la definicion de un metodo
# nombre de variables


class PacienteForm(forms.ModelForm):

    tipo = forms.ModelChoiceField(
        required=True, queryset=TipoPaciente.objects.all())
    codigo = forms.IntegerField(required=False)
    fecha_alta = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.set_initial_values(kwargs)
        self.set_css_controls()

    def set_initial_values(self, kwargs):

        if 'instance' not in kwargs:
            try:
                id_nuevo = int(Paciente.objects.latest('id').id) + 1
                self.fields['codigo'].initial = id_nuevo
            except:
                self.fields['codigo'].initial = 1
        else:
            self.fields['codigo'].initial = self.instance.id

        fecha = datetime.now().date().strftime('%d/%m/%Y')
        self.fields['fecha_alta'].initial = fecha

    def set_css_controls(self):

        self.fields['codigo'].widget.attrs.update({'disabled': 'true'})
        self.fields['fecha_alta'].widget.attrs.update({'disabled': 'true'})

        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    #def clean(self):

        #super(PacienteForm, self).clean()

        #tipo = self.cleaned_data['tipo']
        #nombre = self.cleaned_data['nombre']
        #apellido = self.cleaned_data['apellido']

        #tipo_paciente = TipoPaciente.objects.get(pk=tipo)

        #if tipo_paciente.valor == 'NORMAL':

            #if nombre == '':
                #errors = self._errors.setdefault("nombre", ErrorList())
                #errors.append('Ingrese nombre texto')

            #if apellido == '':
                #errors = self._errors.setdefault("apellido", ErrorList())
                #errors.append('Ingrese apellido texto')

    class Meta:
        model = Paciente
        exclude = ['persona' ]


class PersonaForm(forms.ModelForm):

    instancia = ''

    tipo_documento = forms.ModelChoiceField(
        required=True, queryset=TipoDocumento.objects.all())
    fecha_nacimiento = forms.DateField(initial='01/01/1900', required=True)
    sexo = forms.ModelChoiceField(
        required=True, queryset=Sexo.objects.all())

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        if 'instance' in kwargs:
            self.instancia = kwargs['instance']

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']

        if str.isnumeric(apellido):
            raise forms.ValidationError("Ingrese apellido texto")

        return apellido.upper()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if str.isnumeric(nombre):
            raise forms.ValidationError("Ingrese nombre texto")

        return nombre.upper()

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']

        try:
            datetime.strptime(str(fecha), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha

    def clean_numero_documento(self):
        data = self.cleaned_data['numero_documento']
        if data != '':
            if self.instancia == '':
                persona = Persona.objects.filter(numero_documento=data)
                if len(persona) > 0:
                    paciente = Paciente.objects.filter(persona=persona)
                    if len(paciente) > 0:
                        raise forms.ValidationError('El paciente ya se '
                                                    'encuentra registrado en '
                                                    'el sistema de salud')
            '''
            for i in data:
                if not str.isnumeric(i):
                    raise forms.ValidationError("Una Letra se encuentra "
                                                "dentro del "
                                                "campo Documento")
            '''
        return data

    def clean(self):
        if 'tipo_documento' in self.cleaned_data:
            if 'tipo_documento' != 'S/D':
                if 'numero_documento' in self.cleaned_data:
                    tipo_documento = self.cleaned_data['tipo_documento']
                    numero_documento = self.cleaned_data['numero_documento']
                    tipo = TipoDocumento.objects.filter(abreviatura=tipo_documento).values('longitud')
                    for i in tipo:
                        longitud = i['longitud']
                        if int(len(numero_documento)) > int(longitud):
                            errors = self._errors.setdefault("numero_documento",
                                ErrorList())
                            errors.append('La longitud del Tipo de Documento'
                                ' no corresponde')
                        '''
                        if str(len(numero_documento)) > str(8):
                            errors = self._errors.setdefault("numero_documento",
                                ErrorList())
                            errors.append('La longitud del Tipo de Documento'
                                ' no corresponde')
                        '''
        return super(PersonaForm, self).clean()

    class Meta:
        model = Persona
        fields = '__all__'
        exclude = ['obra_social']

# PacienteFormSet = inlineformset_factory(
#     Persona, Paciente, fields='__all__',
#     exclude=None, form=PersonaForm, formset=PacienteForm, can_delete=False)

