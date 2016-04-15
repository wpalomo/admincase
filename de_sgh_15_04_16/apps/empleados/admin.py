# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Empleado, EmpleadoEspecialidad


class EmpleadoEspecialidadAdmin(admin.ModelAdmin):

    list_display = ['id', 'empleado', 'especialidad']


class EmpleadoAdmin(admin.ModelAdmin):

    list_filter = ['fecha_ingreso']

    list_display = [
        'id',
        'apellido',
        'nombre',
        'documento',
        'fecha_ingreso',
        'fecha_egreso',
    ]

    def apellido(self, empleado):
        return empleado.persona.apellido

    def nombre(self, empleado):
        return empleado.persona.nombre

    def documento(self, empleado):
        return empleado.persona.numero_documento

    search_fields = [
        'id',
        'apellido',
        'nombre',
        'fecha_ingreso',
        'fecha_egreso',
    ]

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(EmpleadoEspecialidad, EmpleadoEspecialidadAdmin)