# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import EmpleadoAgenda


class EmpleadoAgendaAdmin(admin.ModelAdmin):

    search_fields = ['empleado']
    list_display = ['id', 'empleado', 'tiene_agenda']

admin.site.register(EmpleadoAgenda, EmpleadoAgendaAdmin)