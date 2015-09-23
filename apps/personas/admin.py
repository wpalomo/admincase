# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.personas.models import Persona


class PersonaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'apellido',
        'nombre',
        'tipo_documento',
        'numero_documento',
        'sexo',
        'fecha_nacimiento',
        'estado_civil',
        'obra_social',
        'nivel_educacion',
        'profesion',
        'observaciones',
    ]

    list_filter = [
        'numero_documento',
        'apellido',
        'nombre',
        'sexo',
    ]

    search_fields = [
        'numero_documento',
        'apellido',
        'nombre',
        'sexo',
    ]

    ordering = ['apellido']


admin.site.register(Persona, PersonaAdmin)
