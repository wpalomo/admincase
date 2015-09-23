from django.contrib import admin
from apps.domicilios.models import Domicilio, TipoDomicilio


class TipoDomicilioAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion',
    ]


class DomicilioAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion',

    ]


admin.site.register(Domicilio, DomicilioAdmin)
admin.site.register(TipoDomicilio, TipoDomicilioAdmin)