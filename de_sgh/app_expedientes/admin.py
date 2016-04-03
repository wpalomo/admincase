# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import (Expediente, ExpedienteResolucion, ExpedienteDisposicion,
                     ExpedienteServicioMedico, ExpedienteLicitacion,
                     ExpedienteLicitacionCompromiso, ExpedienteLicitacionOrdenado,
                     ExpedienteComodato)

class ExpedienteAdmin(admin.ModelAdmin):

    search_fields = ['numero', 'letra', 'anio']
    list_filter = ['numero', 'letra', 'anio']
    ordering = ['numero']
    list_display = ['id', 'letra', 'numero', 'anio', 'fecha', 'estado']


class ExpedienteResolucionAdmin(admin.ModelAdmin):

    search_fields = ['expediente']
    ordering = ['expediente']
    list_display = ['expediente', 'resolucion_adjudicacion', 'proveedor',
                    'importe', 'numero_resolucion_pago']


class ExpedienteDisposicionAdmin(admin.ModelAdmin):

    search_fields = ['expediente']
    ordering = ['expediente']
    list_display = ['id', 'expediente', 'contratacion_directa', 'proveedor',
                    'importe']


class ExpedienteServicioMedicoAdmin(admin.ModelAdmin):

    search_fields = ['expediente']
    ordering = ['expediente']
    list_display = ['id', 'expediente', 'profesional',
                    'resolucion_contratacion', 'fecha_resolucion_contratacion',
                    'orden_provision', 'acta_recepcion',
                    'numero_resolucion_pago', 'fecha_resolucion_pago',
                    'importe', 'solicitante_resolucion_pago',
                    'fuente_financiamiento']


class ExpedienteLicitacionAdmin(admin.ModelAdmin):

    search_fields = ['expediente']
    ordering = ['expediente']
    list_display = ['id', 'expediente', 'numero', 'anio',
                    'numero_disposicion', 'resolucion_aprobacion',
                    'fecha_resolucion_aprobacion', 'resolucion_adjudicacion',
                    'fecha_resolucion_adjudicacion', 'fuente_financiamiento']


class ExpedienteLicitacionCompromisoAdmin(admin.ModelAdmin):

    search_fields = ['expediente_licitacion']
    ordering = ['expediente_licitacion']
    list_display = ['id', 'expediente_licitacion', 'proveedor', 'monto',
                    'monto_total', 'orden_provision', 'acta_recepcion']



class ExpedienteComodatoAdmin(admin.ModelAdmin):

    search_fields = ['expediente']
    ordering = ['expediente']
    list_display = ['id', 'resolucion_contratacion', 'numero_contratacion_directa', 'importe',
                    'orden_provision', 'resolucion_pago', 'fecha_resolucion_pago', 'solicitante_resolucion_pago']


# class ExpedienteLicitacionOrdenadoAdmin(admin.ModelAdmin):
#
#     search_fields = ['expediente_licitacion']
#     ordering = ['expediente_licitacion']
#     list_display = ['id', 'expediente_licitacion', 'proveedor', 'monto',
#                     'monto_total', 'orden_provision', 'acta_recepcion',
#                     'numero_resolucion_pago', 'fecha_resolucion_pago',
#                     'solicitante_resolucion_pago', 'observaciones']

class ExpedienteLicitacionOrdenadoAdmin(admin.ModelAdmin):

    search_fields = ['expediente_licitacion']
    ordering = ['expediente_licitacion']
    list_display = ['id', 'expediente_licitacion', 'proveedor', 'monto',
                    'monto_total', 'orden_provision', 'acta_recepcion',
                    'numero_resolucion_pago', 'fecha_resolucion_pago',
                    'solicitante_resolucion_pago', 'observaciones']



admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(ExpedienteResolucion, ExpedienteResolucionAdmin)
admin.site.register(ExpedienteDisposicion, ExpedienteDisposicionAdmin)
admin.site.register(ExpedienteServicioMedico, ExpedienteServicioMedicoAdmin)
admin.site.register(ExpedienteLicitacion, ExpedienteLicitacionAdmin)
admin.site.register(ExpedienteLicitacionCompromiso, ExpedienteLicitacionCompromisoAdmin)

admin.site.register(ExpedienteComodato, ExpedienteComodatoAdmin)
# admin.site.register(ExpedienteLicitacionOrdenado,
#                     ExpedienteLicitacionOrdenadoAdmin)

admin.site.register(ExpedienteLicitacionOrdenado, ExpedienteLicitacionOrdenadoAdmin)

