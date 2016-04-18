from django.contrib import admin

from apps.empleados.models import (SituacionLaboral, AsignacionFormal)
from apps.expedientes.models import (Estado, Clase as ClaseExpediente,
                                     Etapa, FuenteFinanciamiento,
                                     NumeroAutoincremental, TipoResolucion,
                                     ServicioAdministracion)

from apps.medicamentos.models import (
    Catalogo, NumeroAutoincremental as NumeroAutoincrementalMedicamento,
    PrincipioActivo, LineaTerapeutica, ViaAdministracion, FormaFarmaceutica)

from .locacion.models import Pais, Provincia, Departamento, Localidad, Barrio
from .obrasocial.models import ObraSocial, MotivoSuspension

from .organigrama.models import (Profesion, Cargo, Direccion,
                                 Departamento as DepartamentoAsignacion,
                                 Division, Servicio, Seccion)

from .persona.models import (Sexo, TipoDocumento, EstadoCivil, NivelEducacion,
                             Parentesco, Etnia)
from .paciente.models import Categoria
from .paciente.models import SituacionLaboral as SituacionLaboralPaciente
from .salud.models import GrupoSanguineo, Especialidad, Practica, UnidadMedida


class SituacionLaboralPacienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class EtniaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class SexoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'abreviatura']

    search_fields = ['descripcion', 'abreviatura']

    ordering = ['descripcion']


class ParentescoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'abreviatura']

    search_fields = ['nombre', 'abreviatura']

    ordering = ['nombre']


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'abreviatura', 'longitud']

    search_fields = ['descripcion', 'abreviatura', 'longitud']

    ordering = ['id']


class EstadoCivilAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'abreviatura']

    search_fields = ['descripcion', 'abreviatura']

    ordering = ['descripcion']


class NivelEducacionAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'abreviatura']
    search_fields = ['descripcion', 'abreviatura']
    ordering = ['descripcion']


class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'abreviatura']
    search_fields = ['nombre', 'abreviatura']
    ordering = ['nombre']


class SituacionLaboralAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'abreviatura']

    search_fields = ['descripcion', 'abreviatura']

    ordering = ['descripcion']


class AsignacionFormalAdmin(admin.ModelAdmin):
    list_display = ['id', 'empleado', 'destino', 'cargo', 'direccion',
                    'departamento', 'division', 'fecha_desde',
                    'fecha_hasta', 'observaciones']

    search_fields = ['destino', 'cargo']

    # ordering = ['destino', 'cargo']
    ordering = ['-empleado']


class PaisAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

    search_fields = ['nombre']

    ordering = ['nombre']


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['nombre']


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['nombre']


class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['nombre']


class BarrioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['nombre']


class ProfesionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id']
    search_fields = ['nombre', 'abreviatura']
    ordering = ['nombre']


class GrupoSanguineoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    ordering = ['id']


class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    ordering = ['nombre']


class PracticaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad']
    search_fields = ['nombre']
    ordering = ['nombre']


# ADMIN COMPLEMENTOS ADMINISTRACION

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'valor']


class ClaseExpedienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'valor']


class TipoResolucionExpedienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'valor']


class ServicioAdministracionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']


class EtapaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'descripcion', 'valor', 'resolucion', 'disposicion',
        'licitacion', 'comodato', 'servicio_medico', 'resoluciones_varias',
        'resolucion_contratacion'
    ]
    ordering = ['id']


class FuenteFinanciamientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cuenta', 'fondo']
    search_fields = ['cuenta']
    ordering = ['cuenta']


class NumeroAutoincrementalAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero', 'tipo']


# FIN ADMIN COMPLEMENTOS ADMINISTRACION

# COMPLEMENTOS FARMACIA MEDICAMENTOS

class PrincipioActivoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']
    ordering = ['id']


class LineaTerapeuticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']
    ordering = ['id']


class ViaAdministracionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']
    ordering = ['id']


class FormaFarmaceuticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'via_administracion', 'descripcion']
    search_fields = ['via_administracion', 'descripcion']
    ordering = ['via_administracion', 'descripcion']


class CatalogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']


class NumeroAutoincrementalMedicamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero', 'tipo']


# FIN COMPLEMENTOS FARMACIA MEDICAMENTOS

class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ['descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'institucion', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class DireccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'institucion', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class DepartamentoAsignacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']


class SeccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']

    search_fields = ['descripcion']

    ordering = ['descripcion']



class MotivoSuspensionAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']
    ordering = ['descripcion']


admin.site.register(Etnia, EtniaAdmin)
admin.site.register(Sexo, SexoAdmin)
admin.site.register(Parentesco, ParentescoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(EstadoCivil, EstadoCivilAdmin)
admin.site.register(NivelEducacion, NivelEducacionAdmin)
# admin.site.register(ObraSocial, ObraSocialAdmin)
admin.site.register(SituacionLaboral, SituacionLaboralAdmin)
admin.site.register(AsignacionFormal, AsignacionFormalAdmin)

admin.site.register(Pais, PaisAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Barrio, BarrioAdmin)

admin.site.register(Profesion, ProfesionAdmin)
admin.site.register(GrupoSanguineo, GrupoSanguineoAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Practica, PracticaAdmin)

admin.site.register(Cargo, CargoAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(DepartamentoAsignacion, DepartamentoAsignacionAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Seccion, SeccionAdmin)

# REGISTRO COMPLEMENTO ADMINISTRACION
admin.site.register(Estado, EstadoAdmin)
admin.site.register(ClaseExpediente, ClaseExpedienteAdmin)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(FuenteFinanciamiento, FuenteFinanciamientoAdmin)
admin.site.register(NumeroAutoincremental, NumeroAutoincrementalAdmin)
admin.site.register(TipoResolucion, TipoResolucionExpedienteAdmin)
admin.site.register(ServicioAdministracion, ServicioAdministracionAdmin)
# FIN REGISTRO COMPLEMENTO ADMINISTRACION

# REGISTRO COMPLEMENTO OBRA SOCIAL
admin.site.register(ObraSocial, ObraSocialAdmin)
admin.site.register(MotivoSuspension, MotivoSuspensionAdmin)
# FIN REGISTRO COMPLEMENTO OBRA SOCIAL

# REGISTRO COMPLEMENTO CATEGORIA PACIENTE
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SituacionLaboralPaciente, SituacionLaboralPacienteAdmin)
# FIN REGISTRO COMPLEMENTO CATEGORIA PACIENTE

# COMPLEMENTOS FARMACIA MEDICAMENTOS
admin.site.register(Catalogo, CatalogoAdmin)
admin.site.register(NumeroAutoincrementalMedicamento,
                    NumeroAutoincrementalMedicamentoAdmin)
admin.site.register(PrincipioActivo, PrincipioActivoAdmin)
admin.site.register(LineaTerapeutica, LineaTerapeuticaAdmin)
admin.site.register(ViaAdministracion, ViaAdministracionAdmin)
admin.site.register(FormaFarmaceutica, FormaFarmaceuticaAdmin)
# FIN COMPLEMENTOS FARMACIA MEDICAMENTOS

admin.site.register(UnidadMedida, UnidadMedidaAdmin)
