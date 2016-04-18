# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import Paciente, TipoPaciente, Clase


class PacienteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'datos_personales',
        'tipo',
    ]

    def datos_personales(self, paciente):
        return str(paciente.persona.apellido) + ", " + \
               str(paciente.persona.nombre) + ", DNI: " + \
               str(paciente.persona.numero_documento)

    list_filter = [
        'persona',
        'tipo',
    ]

    search_fields = [
        'id',
        'persona__apellido',
        'persona__nombre',
        'persona__numero_documento',
        'tipo__valor',
    ]

    ordering = ['persona__apellido']


class TipoPacienteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion',
        'valor',
    ]

    list_filter = [
        'descripcion',
        'valor',
    ]

    search_fields = [
        'descripcion',
        'valor',
    ]

    ordering = ['id']


class ClasePacienteAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['descripcion']


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(TipoPaciente, TipoPacienteAdmin)
admin.site.register(Clase, ClasePacienteAdmin)
