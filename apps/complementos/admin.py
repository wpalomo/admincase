from django.contrib import admin

# from apps.agendas.models import MotivoBloqueo
from apps.clientes.models import SituacionLaboral

from .locacion.models import Pais, Provincia, Departamento, Localidad, Barrio
from .organigrama.models import Profesion, Entidad
from .persona.models import Sexo, TipoDocumento, EstadoCivil, NivelEducacion
from .salud.models import ObraSocial, GrupoSanguineo


class EntidadAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre'
    ]

    search_fields = [
        'id',
        'nombre'
    ]

    ordering = ['nombre']


class SexoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['descripcion']


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['id']


class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['descripcion']


class NivelEducacionAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['descripcion']


class ObraSocialAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'abreviatura'
    ]

    search_fields = [
        'nombre',
        'abreviatura'
    ]

    ordering = ['nombre']


class SituacionLaboralAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'descripcion',
        'abreviatura'
    ]

    search_fields = [
        'descripcion',
        'abreviatura'
    ]

    ordering = ['descripcion']


class PaisAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
    ]

    search_fields = [
        'nombre',
    ]

    ordering = ['nombre']


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
    ]

    search_fields = [
        'nombre',
    ]

    ordering = ['nombre']


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
    ]

    search_fields = [
        'nombre',
    ]

    ordering = ['nombre']


class LocalidadAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
    ]

    search_fields = [
        'nombre',
    ]

    ordering = ['nombre']


class BarrioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
    ]

    search_fields = [
        'nombre',
    ]

    ordering = ['nombre']


class ProfesionAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
    ]

    search_fields = [
        'nombre',
        'abreviatura'
    ]

    ordering = ['nombre']


class GrupoSanguineoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'abreviatura'
    ]

    search_fields = [
        'nombre',
        'abreviatura'
    ]

    ordering = ['nombre']


admin.site.register(Sexo, SexoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(EstadoCivil, EstadoCivilAdmin)
admin.site.register(NivelEducacion, NivelEducacionAdmin)
admin.site.register(ObraSocial, ObraSocialAdmin)
admin.site.register(SituacionLaboral, SituacionLaboralAdmin)

admin.site.register(Pais, PaisAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Barrio, BarrioAdmin)

admin.site.register(Profesion, ProfesionAdmin)
admin.site.register(Entidad, EntidadAdmin)
admin.site.register(GrupoSanguineo, GrupoSanguineoAdmin)