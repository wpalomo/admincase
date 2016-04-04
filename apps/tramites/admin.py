# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.tramites.models import (Tramite, TipoTramite,
                                  Requisito, RequisitoRequerido)


class TramiteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'persona',
        'tipo',
        'fecha_alta',
        'fecha_inicio',
        'fecha_fin',
        'fecha_alarma',
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
        'descripcion',
        'entidad',
        'requisitos_del_tramite'
    ]

    search_fields = [
        'id',
        'nombre',
        'entidad'
    ]

    ordering = ['entidad']

    def requisitos_del_tramite(self, tipotramite):
        lista_requisitos = []
        for req in tipotramite.requisitos.all():
            lista_requisitos.append(req.descripcion)
        return lista_requisitos


class RequisitoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion'
    ]

    search_fields = [
        'id',
        'descripcion'
    ]

    ordering = ['id']


class RequisitoRequeridoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tramite_tipo', 'requisito', 'presentado']

    ordering=['id']

    def tramite_tipo(self, requisitospresentados):
        return requisitospresentados.tramite


admin.site.register(Tramite, TramiteAdmin)
admin.site.register(TipoTramite, TipoTramiteAdmin)
admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(RequisitoRequerido, RequisitoRequeridoAdmin)
