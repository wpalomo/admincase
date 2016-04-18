from django.contrib import admin

from .models import TipoNota, Nota


class TipoNotaAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]


class NotaAdmin(admin.ModelAdmin):

    list_display = [
        'fecha',
        'hora',
        'descripcion',
        'usuario'
    ]

    search_fields = [
        'fecha',
        'hora',
        'descripcion',
        'usuario'
    ]

    list_filter = [
        'fecha',
        'hora',
        'descripcion',
        'usuario'
    ]

admin.site.register(TipoNota, TipoNotaAdmin)
admin.site.register(Nota, NotaAdmin)
