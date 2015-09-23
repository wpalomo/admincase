from django.contrib import admin

from .models import Agenda, AgendaCalendario, TipoAgenda


class AgendaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'empleado',
        'fecha_desde',
        'fecha_hasta',
        'habilitado',
        'tipo_agenda'
    ]

    list_filter = [
         'id',
        'empleado',
        'fecha_desde',
        'fecha_hasta',
        'habilitado',
        'tipo_agenda'
    ]

    search_fields = [
         'id',
        'empleado',
        'fecha_desde',
        'fecha_hasta',
        'habilitado',
        'tipo_agenda'
    ]


class AgendaCalendarioAdmin(admin.ModelAdmin):

    list_filter = [
        'id',
        'agenda',
        'fecha',
        'bloqueado'
    ]

    search_fields = [
        'id',
        'agenda',
        'fecha',
        'bloqueado'
    ]

    list_display = [
        'id',
        'agenda',
        'fecha',
        'bloqueado'
    ]


class TipoAgendaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion'
    ]



admin.site.register(Agenda, AgendaAdmin)
admin.site.register(AgendaCalendario, AgendaCalendarioAdmin)
admin.site.register(TipoAgenda, TipoAgendaAdmin)

