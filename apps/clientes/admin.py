# -*- encoding: utf-8 -*-
from django.contrib import admin

from apps.clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'persona',
        'documento',
        'cuil',
        'fecha_alta_sistema',
        'situacion_laboral'
    ]

    list_filter = [
        'cuil',
        'fecha_alta_sistema',
        'situacion_laboral'
    ]

    search_fields = [
        'cuil',
        'fecha_alta_sistema',
        'situacion_laboral'
    ]

    ordering = ['id']

    def persona(self, cliente):
        return cliente.persona

    def documento(self, cliente):
        return str(cliente.persona.tipo_documento) + ' N°: ' + str(
            cliente.persona.numero_documento)

admin.site.register(Cliente, ClienteAdmin)
