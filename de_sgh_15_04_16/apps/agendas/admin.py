from django.contrib import admin

from .models import (Agenda, TipoAgenda, Dia, AgendaDiaConfiguracion,
                     MotivoBloqueo)


class AgendaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'institucion',
        'profesional',
        'fecha_desde',
        'fecha_hasta',
        'especialidad',
        'tipo_agenda'
    ]

    list_filter = ['institucion']


class TipoAgendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']


class DiaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'numero']


class AgendaDiaConfiguracionAdmin(admin.ModelAdmin):
    list_display = [
        'agenda',
        'dia',
        'fecha_desde',
        'fecha_hasta',
        'hora_desde',
        'hora_hasta',
        'duracion_minutos',
        'practica'
        ]


class MotivoBloqueoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']


admin.site.register(Agenda, AgendaAdmin)
admin.site.register(TipoAgenda, TipoAgendaAdmin)
admin.site.register(Dia, DiaAdmin)
admin.site.register(AgendaDiaConfiguracion, AgendaDiaConfiguracionAdmin)
admin.site.register(MotivoBloqueo, MotivoBloqueoAdmin)