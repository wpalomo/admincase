
from datetime import datetime, date

from django import forms

from apps.complementos.salud.models import Especialidad, Practica
from apps.empleados.models import Empleado
from apps.instituciones.models import Institucion
from apps.seguridad.models import EmpleadoAgenda

from . import helpers

from .models import (Agenda, TipoAgenda, Dia, AgendaDiaConfiguracion,
                     AgendaFechaDetalle, AgendaDiaConfiguracionBloqueo,
                     MotivoBloqueo)


class AgendaForm(forms.ModelForm):

    institucion = forms.ModelChoiceField(
        required=True, queryset=Institucion.objects.all())
    profesional = forms.ModelChoiceField(required=True, queryset=[])
    fecha_desde = forms.DateField(required=True)
    fecha_hasta = forms.DateField(required=True)
    especialidad = forms.ModelChoiceField(required=True,
        queryset=[])
    tipo_agenda = forms.ModelChoiceField(
        required=True, queryset=TipoAgenda.objects.all())

    def __init__(self, *args, **kwargs):
        super(AgendaForm, self).__init__(*args, **kwargs)

        self.es_modificacion = kwargs.get('instance', False)

        self.set_queryset_profesional()
        self.set_css_controls()
        self.set_initial_values()

    def set_initial_values(self):

        fecha = datetime.now()
        fecha = fecha.strftime('%d/%m/%Y')
        self.fields['fecha_desde'].initial = fecha
        self.fields['fecha_hasta'].initial = fecha

        self.fields['especialidad'].queryset = Especialidad.objects.all()

    def set_queryset_profesional(self):

        empleados_permisos = \
            [emp['empleado_id'] for emp in EmpleadoAgenda.objects.filter(
                tiene_agenda=True).values('empleado_id')]

        self.fields['profesional'].queryset = \
                Empleado.objects.filter(pk__in=empleados_permisos)

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_fecha_desde(self):
        fecha_desde = self.cleaned_data['fecha_desde']

        try:
            datetime.strptime(str(fecha_desde), '%Y-%m-%d')

            fecha_actual = date.today()

            if not self.es_modificacion:
                if fecha_desde < fecha_actual:
                    raise forms.ValidationError(
                        'La fecha Desde no debe ser MENOR a la actual')

        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_desde

    def clean_fecha_hasta(self):

        fecha_hasta = self.cleaned_data['fecha_hasta']

        try:
            datetime.strptime(str(fecha_hasta), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha no valida")

        try:
            fecha_desde = self.cleaned_data['fecha_desde']
        except KeyError:
            return fecha_hasta

        datetime.strptime(str(fecha_desde), '%Y-%m-%d')

        if fecha_desde > fecha_hasta:
            raise forms.ValidationError(
                'La FECHA HASTA debe ser MAYOR a FECHA DESDE')

        return fecha_hasta

    def clean(self):
        super(AgendaForm, self).clean()

        try:
            self.cleaned_data['fecha_desde']
            self.cleaned_data['fecha_hasta']
            self.cleaned_data['tipo_agenda']
            hay_error = False
        except KeyError:
            hay_error = True

        if not hay_error:
            agenda = self.obtener_objeto_modelo()

            if helpers.hay_superposicion_entre_agendas(agenda):
                print("ERRORORRORORRORO")
                raise forms.ValidationError('SUPERPOSICION ENTRE AGENDAS!!!')

    def obtener_objeto_modelo(self):

        if self.es_modificacion:
            agenda_id = self.es_modificacion.id
        else:
            agenda_id = 0

        agenda = Agenda(
            id=agenda_id,
            institucion=self.cleaned_data['institucion'],
            profesional=self.cleaned_data['profesional'],
            fecha_desde=self.cleaned_data['fecha_desde'],
            fecha_hasta=self.cleaned_data['fecha_hasta'],
            especialidad=self.cleaned_data['especialidad'],
            tipo_agenda=self.cleaned_data['tipo_agenda']
        )

        return agenda

    class Meta:
        model = Agenda
        fields = '__all__'


class AgendaDiaConfiguracionForm(forms.ModelForm):

    dia = forms.ModelChoiceField(required=True, queryset=Dia.objects.all())
    fecha_desde = forms.DateField(required=True)
    fecha_hasta = forms.DateField(required=True)
    hora_desde = forms.TimeField(required=True)
    hora_hasta = forms.TimeField(required=True)
    duracion_minutos = forms.IntegerField(required=True)
    practica = forms.ModelChoiceField(required=False, queryset=[])

    def __init__(self, especialidad, *args, **kwargs):
        super(AgendaDiaConfiguracionForm, self).__init__(*args, **kwargs)
        self.set_css_controls()

        self.fields['practica'].queryset = Practica.objects.filter(
            especialidad__id=especialidad)

        self.instancia = kwargs.get('instance', False)

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_hora_desde(self):

        hora = self.cleaned_data['hora_desde']

        try:
            datetime.strptime(str(hora), '%H:%M:%S').time()

        except ValueError:
            raise ValueError("HORA no valida. Ingrese hh:mm")

        return hora

    def clean_hora_hasta(self):

        hora = self.cleaned_data['hora_hasta']

        try:
            datetime.strptime(str(hora), '%H:%M:%S').time()

        except ValueError:
            raise ValueError("HORA no valida. Ingrese hh:mm")

        return hora

    def clean_fecha_desde(self):

        fecha_desde = self.cleaned_data['fecha_desde']

        try:
            datetime.strptime(str(fecha_desde), '%Y-%m-%d')

            agenda = self.cleaned_data['agenda']

            if fecha_desde < agenda.fecha_desde:
                raise forms.ValidationError(
                    'FECHA DESDE fuera de Rango de fechas de la Agenda')

        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_desde

    def clean_fecha_hasta(self):

        fecha_hasta = self.cleaned_data['fecha_hasta']

        try:
            datetime.strptime(str(fecha_hasta), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha no valida")

        try:
            fecha_desde = self.cleaned_data['fecha_desde']
        except KeyError:
            return fecha_hasta

        datetime.strptime(str(fecha_desde), '%Y-%m-%d')

        if fecha_desde > fecha_hasta:
            raise forms.ValidationError(
                'La FECHA HASTA debe ser MAYOR a FECHA DESDE')

        agenda = self.cleaned_data['agenda']

        if fecha_hasta > agenda.fecha_hasta:
            raise forms.ValidationError(
                'FECHA HASTA fuera de Rango de fechas de la Agenda')

        return fecha_hasta

    def clean(self):
        super(AgendaDiaConfiguracionForm, self).clean()

        try:
            self.cleaned_data['fecha_desde']
            self.cleaned_data['fecha_hasta']
            self.cleaned_data['hora_desde']
            self.cleaned_data['hora_hasta']
            hay_error = False
        except KeyError:
            hay_error = True

        if not hay_error:
            dia_configuracion = self.obtener_objeto_modelo()

            if helpers.hay_superposicion_fecha_hora(dia_configuracion):
                raise forms.ValidationError('SUPERPOSICION DE FECHA Y HORA!!!')

    def obtener_objeto_modelo(self):

        dia_configuracion_id = self.instancia.id if self.instancia else 0

        try:
            practica = self.cleaned_data['practica']
        except:
            practica = None

        dia_configuracion = AgendaDiaConfiguracion(
            id=dia_configuracion_id,
            agenda=self.cleaned_data['agenda'],
            dia=self.cleaned_data['dia'],
            fecha_desde=self.cleaned_data['fecha_desde'],
            fecha_hasta=self.cleaned_data['fecha_hasta'],
            hora_desde=self.cleaned_data['hora_desde'],
            hora_hasta=self.cleaned_data['hora_hasta'],
            duracion_minutos=self.cleaned_data['duracion_minutos'],
            practica=practica,
        )

        return dia_configuracion

    class Meta:
        model = AgendaDiaConfiguracion
        fields = '__all__'


class AgendaFechaDetalleForm(forms.ModelForm):

    fecha = forms.DateField(required=True)
    hora_desde = forms.TimeField(required=True)
    hora_hasta = forms.TimeField(required=True)
    duracion_minutos = forms.IntegerField(required=True)
    practica = forms.ModelChoiceField(required=False, queryset=[])

    def __init__(self, especialidad, *args, **kwargs):
        super(AgendaFechaDetalleForm, self).__init__(*args, **kwargs)
        self.set_css_controls()

        self.fields['practica'].queryset = Practica.objects.filter(
            especialidad__id=especialidad)

    def set_css_controls(self):
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean_hora_desde(self):

        hora = self.cleaned_data['hora_desde']

        try:
            datetime.strptime(str(hora), '%H:%M:%S').time()

        except ValueError:
            raise ValueError("HORA no valida. Ingrese hh:mm")

        return hora

    def clean_hora_hasta(self):

        hora = self.cleaned_data['hora_hasta']

        try:
            datetime.strptime(str(hora), '%H:%M:%S').time()

        except ValueError:
            raise ValueError("HORA no valida. Ingrese hh:mm")

        return hora

    class Meta:
        model = AgendaFechaDetalle
        fields = '__all__'

# -------------------
# BLOQUEOS DE AGENDA
# -------------------


class AgendaBloqueoForm(forms.ModelForm):

    bloqueo_por_fecha_fecha = forms.ModelChoiceField(
        queryset=[], required=False)
    bloqueo_por_fecha_motivo_bloqueo = forms.ModelChoiceField(
        queryset=MotivoBloqueo.objects.all(), required=False)
    bloqueo_por_fecha_observaciones = forms.CharField(required=False)

    bloqueo_por_periodo_fecha_desde = forms.DateField(required=False)
    bloqueo_por_periodo_fecha_hasta = forms.DateField(required=False)
    bloqueo_por_periodo_motivo_bloqueo = forms.ModelChoiceField(
        queryset=MotivoBloqueo.objects.all(), required=False)
    bloqueo_por_periodo_observaciones = forms.CharField(required=False)

    def __init__(self, agenda, *args, **kwargs):
        super(AgendaBloqueoForm, self).__init__(*args, **kwargs)
        self.set_initial_values(agenda)

    def set_initial_values(self, agenda):
        self.fields['bloqueo_por_fecha_fecha'].queryset = \
            AgendaFechaDetalle.objects.filter(agenda__id=agenda)

    class Meta:
        model = MotivoBloqueo
        fields = '__all__'
        exclude = ['descripcion']


class AgendaDiaConfiguracionBloqueoForm(forms.ModelForm):

    fecha_desde = forms.DateField(required=True)
    fecha_hasta = forms.DateField(required=True)
    motivo_bloqueo = forms.ModelChoiceField(
        required=True, queryset=MotivoBloqueo.objects.all())
    observacion = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(AgendaDiaConfiguracionBloqueoForm, self).__init__(*args, **kwargs)

    def clean_fecha_desde(self):

        fecha_desde = self.cleaned_data['fecha_desde']

        try:
            datetime.strptime(str(fecha_desde), '%Y-%m-%d')

            dia_configuracion = self.cleaned_data['dia_configuracion']

            if fecha_desde < dia_configuracion.fecha_desde:
                raise forms.ValidationError(
                    'FECHA DESDE fuera de Rango de fechas')

        except ValueError:
            raise ValueError("Fecha no valida")

        return fecha_desde

    def clean_fecha_hasta(self):

        fecha_hasta = self.cleaned_data['fecha_hasta']

        try:
            datetime.strptime(str(fecha_hasta), '%Y-%m-%d')
        except ValueError:
            raise ValueError("Fecha no valida")

        try:
            fecha_desde = self.cleaned_data['fecha_desde']
        except KeyError:
            return fecha_hasta

        datetime.strptime(str(fecha_desde), '%Y-%m-%d')

        if fecha_desde > fecha_hasta:
            raise forms.ValidationError(
                'La FECHA HASTA debe ser MAYOR a FECHA DESDE')

        dia_configuracion = self.cleaned_data['dia_configuracion']

        if fecha_hasta > dia_configuracion.fecha_hasta:
            raise forms.ValidationError(
                'FECHA HASTA fuera de Rango de fechas')

        return fecha_hasta

    class Meta:
        model = AgendaDiaConfiguracionBloqueo
        fields = '__all__'