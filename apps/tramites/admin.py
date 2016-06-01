# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.tramites.models import (Tramite, TipoTramite,
                                  Requisito, RequisitoTipoTramite,
                                  RequisitoTramite)


class TramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'cliente',
        'tipo',
        'fecha_alta',
        'fecha_turno',
        'fecha_alarma',
        'fecha_fin',
        'estado',
        'observaciones'
    ]

    search_fields = [
        'id',
        'cliente',
        'tipo'
    ]

    ordering = ['tipo']


class TipoTramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion',
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
        'descripcion',
        'valor'
    ]

    search_fields = [
        'id',
        'descripcion'
    ]

    ordering = ['id']


class RequisitoTipoTramiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_tramite', 'requisito', 'estado']

    ordering = ['tipo_tramite']


class RequisitoTramiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'tramite', 'requisito', 'presentado']

    ordering = ['id']


admin.site.register(Tramite, TramiteAdmin)
admin.site.register(TipoTramite, TipoTramiteAdmin)
admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(RequisitoTipoTramite, RequisitoTipoTramiteAdmin)
admin.site.register(RequisitoTramite, RequisitoTramiteAdmin)
