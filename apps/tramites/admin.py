# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.tramites.models import Tramite, TipoTramite


class TramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'persona',
        'tipo',
        'entidad'
    ]

    search_fields = [
        'id',
        'persona',
        'tipo',
        'entidad'
    ]

    ordering = ['tipo']


class TipoTramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nombre',
        'estado',
        'observaciones'
    ]

    search_fields = [
        'nombre',
        'estado'
    ]

    ordering = ['nombre']

admin.site.register(Tramite, TramiteAdmin)
admin.site.register(TipoTramite, TipoTramiteAdmin)
