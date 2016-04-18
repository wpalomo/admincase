# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.personas.models import Persona, PersonaObraSocial, Profesion


class PersonaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'apellido',
        'nombre',
        'tipo_documento',
        'numero_documento',
        'sexo',
        'foto',
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


class PersonaObraSocialAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'persona',
        'obra_social',
        'numero_afiliado',
        'fecha_emision',
        'fecha_vencimiento',
        'tipo_beneficiario',
        'parentesco',
        'categoria',
        'habitual',
        'suspendida',
        'motivo_suspension',
        'observacion',
    ]

    list_filter = [
        'obra_social',
        'numero_afiliado',
        'fecha_emision',
        'fecha_vencimiento',
    ]

    search_fields = [
        'obra_social',
        'numero_afiliado',
    ]

    ordering = ['obra_social']

admin.site.register(Persona, PersonaAdmin)
admin.site.register(PersonaObraSocial, PersonaObraSocialAdmin)
