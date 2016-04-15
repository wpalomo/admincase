# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import (Medicamento, Composicion, MedicamentoLineaTerapeutica,
                     AdministracionForma, MedicamentoLaboratorio, Laboratorio,
                     Envase, Agrupado, Pack, Pallet)


class MedicamentoAdmin(admin.ModelAdmin):

    search_fields = ['catalogo', 'codigo', 'denominacion']
    list_filter = ['catalogo', 'codigo', 'denominacion']
    ordering = ['codigo']
    list_display = ['id', 'catalogo', 'codigo', 'denominacion',
                    'producto_combinado', 'libre_azucar', 'libre_conservante',
                    'libre_cfc', 'libre_gluten']


class ComposicionAdmin(admin.ModelAdmin):

    search_fields = ['medicamento', 'principio_activo']
    ordering = ['medicamento']
    list_display = ['id', 'medicamento', 'principio_activo',
                    'potencia_numerador',
                    'potencia_denominador']


class MedicamentoLineaTerapeuticaAdmin(admin.ModelAdmin):

    search_fields = ['medicamento', 'linea_terapeutica']
    ordering = ['linea_terapeutica']
    list_display = ['id', 'medicamento', 'linea_terapeutica']


class AdministracionFormaAdmin(admin.ModelAdmin):

    search_fields = ['medicamento', 'via_administracion', 'forma_farmaceutica']
    ordering = ['via_administracion', 'medicamento']
    list_display = ['id', 'medicamento', 'via_administracion',
                    'forma_farmaceutica']

# --- Laboratorio ---- #


class PalletAdmin(admin.ModelAdmin):

    list_display = ['descripcion']
    search_fields = ['descripcion']
    list_filter = ['descripcion']


class PackAdmin(admin.ModelAdmin):

    list_display = ['descripcion']
    search_fields = ['descripcion']
    list_filter = ['descripcion']


class AgrupadoAdmin(admin.ModelAdmin):

    list_display = ['descripcion']
    search_fields = ['descripcion']
    list_filter = ['descripcion']


class EnvaseAdmin(admin.ModelAdmin):

    list_display = ['descripcion']
    search_fields = ['descripcion']
    list_filter = ['descripcion']


class FormaFarmaceuticaAdmin(admin.ModelAdmin):

    list_display = ['via_administracion', 'descripcion']
    search_fields = ['descripcion']
    list_filter = ['descripcion']


class LaboratorioAdmin(admin.ModelAdmin):

    search_fields = ['descripcion']
    list_filter = ['descripcion']
    list_display = ['descripcion']


class MedicamentoLaboratorioAdmin(admin.ModelAdmin):

    def medicamento(self, medicamentolaboratorio):
        return medicamentolaboratorio.Medicamento.codigo

    def forma_farmaceutica(self, formafarmaceutica):
        return formafarmaceutica.FormaFarmaceutica.descripcion

    def envase_primario(self, envase):
        return envase.Envase.descripcion

    def agrupado(self, agrupado):
        return agrupado.Agrupado.descripcion

    def pack_unidad_despacho(self, pack):
        return pack.Pack.descripcion

    def pallet_unidad_logistica(self, pallet):
        return pallet.Pallet.descripcion

    search_fields = ['nombre_comercial', 'numero_certificado', 'numero_gtin',
                     'cantidad_envase_primario', 'cantidad_envase_secundario']
    list_filter = ['nombre_comercial', 'numero_certificado', 'numero_gtin',
                   'cantidad_envase_primario', 'cantidad_envase_secundario']
    list_display = ['medicamento', 'nombre_comercial', 'laboratorio',
                    'numero_certificado', 'numero_gtin', 'forma_farmaceutica',
                    'envase_primario', 'cantidad_envase_primario',
                    # 'unidad_medida_envase_primario', 'envase_secundario',
                    'envase_secundario',
                    'cantidad_envase_secundario',
                    # 'unidad_medida_envase_secundario', 'agrupado_unidad',
                    'agrupado_unidad',
                    'pack_unidad_despacho', 'pallet_unidad_logistica',
                    'imagen_medicamento', 'prospecto_medicamento']


admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Composicion, ComposicionAdmin)
admin.site.register(MedicamentoLineaTerapeutica,
                    MedicamentoLineaTerapeuticaAdmin)
admin.site.register(AdministracionForma, AdministracionFormaAdmin)

admin.site.register(Pallet, PalletAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(Agrupado, AgrupadoAdmin)
admin.site.register(Envase, EnvaseAdmin)
admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(MedicamentoLaboratorio, MedicamentoLaboratorioAdmin)
