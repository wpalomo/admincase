# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.tramites.models import Tramite, TipoTramite, Requisito


class TramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'persona',
        'tipo',
        'estado',
        'observaciones'
    ]

    search_fields = [
        'id',
        'persona',
        'tipo'
    ]

    ordering = ['tipo']


class TipoTramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nombre',
        'entidad'
    ]

    search_fields = [
        'id',
        'nombre',
        'entidad'
    ]

    ordering = ['entidad']


class RequisitoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nombre',
        'tipo_tramite'
    ]

    search_fields = [
        'id',
        'nombre',
        'tipo_tramite'
    ]

    ordering = ['tipo_tramite']

admin.site.register(Tramite, TramiteAdmin)
admin.site.register(TipoTramite, TipoTramiteAdmin)
admin.site.register(Requisito, RequisitoAdmin)
