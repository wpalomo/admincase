from django.contrib import admin

from .models import Familiar, FamiliarPaciente
from apps.complementos.locacion.models import LugarNacimiento


class FamiliarAdmin(admin.ModelAdmin):

    list_display = [
        'persona'
    ]

    list_filter = [
        'persona'
    ]


class FamiliarPacienteAdmin(admin.ModelAdmin):

    list_display = [
        'parentesco',
        'tipo_relacion'
    ]

    list_filter = [
        'parentesco',
        'tipo_relacion'
    ]

    search_fields = [
        'parentesco',
        'tipo_relacion'
    ]


class LugarNacimientoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        # 'pais'
    ]

admin.site.register(Familiar, FamiliarAdmin)
admin.site.register(FamiliarPaciente, FamiliarPacienteAdmin)
admin.site.register(LugarNacimiento, LugarNacimientoAdmin)
