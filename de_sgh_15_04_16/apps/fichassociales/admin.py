from django.contrib import admin

from .models import FichaSocial, SituacionPropiedad, TipoVivienda, \
    TerrenoPropio, TipoConstruccion, ServicioAgua, ServicioLuzElectrica, \
    OtroServicio, TipoProgramaSocial, TipoBanio, TipoTecho, TipoPared, \
    TipoPiso, TipoIVA


class SituacionPropiedadAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoViviendaAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TerrenoPropioAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class FichaSocialAdmin(admin.ModelAdmin):

    list_display = [
        'paciente',
        'numero_ficha',
        'ultima_verificacion',
        'tipo_iva',
        'lugar_trabajo',
        'pais',
        'provincia',
        'departamento',
        'localidad',
        'barrio',
        'descripcion_domicilio',
        'codigo_postal',
        'situacion_propiedad',
        'tipo_vivienda',
        'terreno_propio',
        'tipo_construccion',
        'servicio_agua',
        'servicio_luz_electrica',
        'observacion_socio_economica'
    ]

    search_fields = [
        'numero_ficha',
        'ultima_verificacion',
    ]

    list_filter = [
        'numero_ficha',
        'ultima_verificacion',
    ]


class TipoConstruccionAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class ServicioAguaAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class ServicioLuzElectricaAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class OtroServicioAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoBanioAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoTechoAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoParedAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoPisoAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoProgramaSocialAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


class TipoIVAAdmin(admin.ModelAdmin):

    list_filter = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]


admin.site.register(FichaSocial, FichaSocialAdmin)
admin.site.register(TipoIVA, TipoIVAAdmin)
# ASPECTOS HABITACIONALES
admin.site.register(TipoPiso, TipoPisoAdmin)
admin.site.register(TipoPared, TipoParedAdmin)
admin.site.register(TipoTecho, TipoTechoAdmin)
admin.site.register(TipoBanio, TipoBanioAdmin)
admin.site.register(OtroServicio, OtroServicioAdmin)
admin.site.register(ServicioLuzElectrica, ServicioLuzElectricaAdmin)
admin.site.register(ServicioAgua, ServicioAguaAdmin)
admin.site.register(TipoConstruccion, TipoConstruccionAdmin)
admin.site.register(TerrenoPropio, TerrenoPropioAdmin)
admin.site.register(TipoVivienda, TipoViviendaAdmin)
admin.site.register(SituacionPropiedad, SituacionPropiedadAdmin)
# PROGRAMAS SOCIALES
admin.site.register(TipoProgramaSocial, TipoProgramaSocialAdmin)
